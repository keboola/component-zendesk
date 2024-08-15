import os
import logging
from collections import OrderedDict
from typing import List

import dlt
from dlt.common import pendulum
from dlt.common.time import ensure_pendulum_datetime
from duckdb import duckdb
from keboola.component.base import ComponentBase, sync_action
from keboola.component.dao import ColumnDefinition, BaseType, SupportedDataTypes
from keboola.component.exceptions import UserException
from keboola.component.sync_actions import SelectElement
from kbcstorage.client import Client

from configuration import Configuration

from dlt_zendesk import zendesk_support, zendesk_mapping

DLT_TMP_DIR = "/tmp/.dlt"
DUCKDB_TMP_DIR = "/tmp/.dlt"
DATASET_NAME = "zendesk_data"
PIPELINE_NAME = "dlt_zendesk_pipeline"

DEFAULT_START_DATE = pendulum.datetime(year=2000, month=1, day=1)


class Component(ComponentBase):
    def __init__(self):
        super().__init__()
        self.params = None
        self.pipeline_destination = None
        self.connection = None
        self.pipeline_name = None
        self.dataset_name = None

    def run(self):
        """
        Main execution code
        """
        self.params = Configuration(**self.configuration.parameters)

        # create the actual start time here for elimination possible data gaps
        actual_start = pendulum.now().int_timestamp

        # get the previous start time
        if self.params.sync_options.is_incremental:
            previous_start = self.get_state_file().get("time", {}).get("previousStart", DEFAULT_START_DATE)
            logging.info(f"Incremental load mode - previous start date is {previous_start}")
        else:
            previous_start = DEFAULT_START_DATE
            logging.info(f"Full sync mode load is disabled - starting from the default date {previous_start}")
        load_from_iso: int = ensure_pendulum_datetime(previous_start).int_timestamp

        # set the DLT environment
        self._set_dlt()

        # run the pipeline
        loaded_tables = self._run_dlt_pipeline(load_from_iso)

        # initialize the connection
        self._init_connection(duck_db_file=self.duckdb_file)

        # prepare the views
        views_to_export = self._prepare_views(loaded_tables)

        # export views to the CSV
        self._export_views(views_to_export)

        # save the state
        logging.info(f"Saving the state file with the actual start date {actual_start}")
        self.write_state_file({"time": {"previousStart": actual_start}})

    def _set_dlt(self):
        # prepare the temporary directories
        os.makedirs(DLT_TMP_DIR, exist_ok=True)
        os.makedirs(DUCKDB_TMP_DIR, exist_ok=True)

        # set the environment variables
        os.environ["DLT_DATA_DIR"] = DLT_TMP_DIR
        os.environ["RUNTIME__DLTHUB_TELEMETRY"] = "false"
        os.environ["RUNTIME__LOG_LEVEL"] = "DEBUG" if self.params.debug else "CRITICAL"
        os.environ["SOURCES__CREDENTIALS__SUBDOMAIN"] = self.params.authentication.sub_domain
        os.environ["SOURCES__CREDENTIALS__EMAIL"] = self.params.authentication.email
        os.environ["SOURCES__CREDENTIALS__TOKEN"] = self.params.authentication.api_token
        os.environ["EXTRACT__WORKERS"] = "40"
        os.environ["EXTRACT__MAX_PARALLEL_ITEMS"] = "100"
        os.environ["NORMALIZE__WORKERS"] = "40"
        os.environ["LOAD__WORKERS"] = "40"

        # set the dataset and pipeline names
        self.dataset_name = DATASET_NAME
        self.pipeline_name = PIPELINE_NAME
        self.duckdb_file = f"{DUCKDB_TMP_DIR}/{self.pipeline_name}.duckdb"

        # check if the duckdb file exists delete it - especially for the local run
        if os.path.exists(self.duckdb_file):
            os.remove(self.duckdb_file)
        # set the duckdb connection
        config = dict(threads="6",
                      memory_limit="1024MB",
                      max_memory="1024MB")

        conn = duckdb.connect(self.duckdb_file, config=config)
        self.pipeline_destination = dlt.destinations.duckdb(conn)

    def _run_dlt_pipeline(self, start_date_iso) -> list:
        # prepare the pipeline
        logging.info("Preparing DLT pipeline")
        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination=self.pipeline_destination,
            dataset_name=self.dataset_name,
            progress="log",

        )

        # filter the source by selected details
        logging.info("Filtering the source by selected details")
        source = zendesk_support(start_date_iso)
        for key, value in self.params.available_details.dict().items():
            source.resources[key].selected = value

        # run the pipeline
        logging.info("Running the DLT pipeline")
        pipeline = pipeline.run(source, refresh="drop_sources")
        logging.info("Pipeline finished")
        pipeline.raise_on_failed_jobs()

        # get the loaded tables
        logging.debug("Getting the loaded tables")
        loaded_tables = []
        for package in pipeline.load_packages:
            jobs = package.jobs.get("completed_jobs", [])
            for job in jobs:
                table = job.job_file_info.table_name
                if not table.startswith("dlt_"):
                    loaded_tables.append(table)

        return loaded_tables

    def _prepare_views(self, loaded_tables):
        logging.info("Preparing output views")
        # set the database
        self.connection.execute(f"USE {self.dataset_name};")

        # create output views
        prepared_views = []
        for view in zendesk_mapping.views:
            # if is created all tables for view
            if all(t in loaded_tables for t in view.source_tables):
                logging.info(f"Creating output view {view.name}")
                self.connection.execute(view.query)
                prepared_views.append(view)
            else:
                logging.info(f"View {view.name} was not created due to missing tables probably due to an filter ")
        return prepared_views

    def _export_views(self, views):
        logging.info("Exporting views to CSV")
        for view in views:
            # get the schema of the view
            table_meta = self.connection.execute(f"""DESCRIBE {view.name};""").fetchall()
            schema = OrderedDict(
                (c[0], ColumnDefinition(data_types=BaseType(dtype=self.convert_base_types(c[1])))) for c in table_meta)

            # prepare the out table
            out_table = self.create_out_table_definition(f"{view.name}.csv",
                                                         schema=schema,
                                                         primary_key=view.primary_key,
                                                         incremental=self.params.destination.is_incremental_load_type,
                                                         destination=".".join(
                                                             filter(None, [self.params.destination.destination_bucket,
                                                                           view.name])),
                                                         has_header=True,
                                                         )
            # export the view
            logging.info(f"Exporting view {view.name}")
            try:
                # ../data/out/tables/{view.name}.csv
                export_query = f"""COPY '{view.name}' TO '{out_table.full_path}'
                                                (HEADER false, DELIMITER ',', FORCE_QUOTE *)"""
                self.connection.execute(export_query)
            except duckdb.ConversionException as e:
                raise Exception(f"Error during query execution: {e}")

            # write the manifest
            self.write_manifest(out_table)

    @staticmethod
    def convert_base_types(dtype: str) -> SupportedDataTypes:
        if dtype in ['TINYINT', 'SMALLINT', 'INTEGER', 'BIGINT', 'HUGEINT',
                     'UTINYINT', 'USMALLINT', 'UINTEGER', 'UBIGINT', 'UHUGEINT']:
            return SupportedDataTypes.INTEGER
        elif dtype in ['REAL', 'DECIMAL']:
            return SupportedDataTypes.NUMERIC
        elif dtype == 'DOUBLE':
            return SupportedDataTypes.FLOAT
        elif dtype == 'BOOLEAN':
            return SupportedDataTypes.BOOLEAN
        elif dtype in ['TIMESTAMP', 'TIMESTAMP WITH TIME ZONE']:
            return SupportedDataTypes.TIMESTAMP
        elif dtype == 'DATE':
            return SupportedDataTypes.DATE
        else:
            return SupportedDataTypes.STRING

    def _init_connection(self, duck_db_file):
        logging.debug(f"Initializing connection to DuckDB database {duck_db_file}")
        self.connection = duckdb.connect(duck_db_file)

    def _get_kbc_root_url(self):
        return f'https://{self.environment_variables.stack_id}'

    def _get_storage_token(self) -> str:
        return self.configuration.parameters.get('#storage_token') or self.environment_variables.token

    @sync_action('get_buckets')
    def get_buckets(self) -> List[SelectElement]:
        """
        Sync action for getting list of available buckets
        Returns:
            List[SelectElement]: List of available buckets
        """
        sapi_client = Client(self._get_kbc_root_url(), self._get_storage_token())

        buckets = sapi_client.buckets.list()
        return [SelectElement(value=b['id'], label=f'{b["id"]} ({b["name"]})') for b in buckets]


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
