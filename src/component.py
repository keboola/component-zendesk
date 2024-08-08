import os
import logging
from collections import OrderedDict
from typing import Any

import dlt
from dlt.common import pendulum
from dlt.common.time import ensure_pendulum_datetime
from duckdb import duckdb
from keboola.component.base import ComponentBase
from keboola.component.dao import ColumnDefinition, BaseType, SupportedDataTypes
from keboola.component.exceptions import UserException

from configuration import Configuration

from dlt_zendesk_client import zendesk_support
from src.dlt_zendesk_client import zendesk_mapping

DLT_TMP_DIR = "/tmp/.dlt"
DUCKDB_TMP_DIR = "/tmp/.dlt"
DATASET_NAME = "zendesk_data"
PIPELINE_NAME = "dlt_zendesk_pipeline"

DEFAULT_START_DATE = pendulum.datetime(year=2000, month=1, day=1)


class Component(ComponentBase):
    def __init__(self):
        super().__init__()
        self.pipeline_destination = None
        self.connection = None
        self.pipeline_name = None
        self.dataset_name = None

    def run(self):
        """
        Main execution code
        """
        params = Configuration(**self.configuration.parameters)

        # create the actual start time here for elimination possible data gaps
        actual_start = pendulum.now().int_timestamp

        # get the previous start time
        previous_start = self.get_state_file().get("time", {}).get("previousStart", DEFAULT_START_DATE)
        load_from_iso: int = ensure_pendulum_datetime(previous_start).int_timestamp

        # set the DLT environment
        self._set_dlt(params)

        # run the pipeline
        loaded_tables = self._run_dlt_pipeline(load_from_iso)

        # initialize the connection
        self._init_connection(duck_db_file=self.duckdb_file)

        # prepare the views
        views_to_export = self._prepare_views(loaded_tables)

        # export views to the CSV
        self._export_views(views_to_export)

        # save the state
        self.write_state_file({"time": {"previousStart": actual_start}})

    def _set_dlt(self, params):
        # prepare the temporary directories
        os.makedirs(DLT_TMP_DIR, exist_ok=True)
        os.makedirs(DUCKDB_TMP_DIR, exist_ok=True)

        # set the environment variables
        os.environ["DLT_DATA_DIR"] = DLT_TMP_DIR
        os.environ["RUNTIME__DLTHUB_TELEMETRY"] = "false"
        os.environ["RUNTIME__LOG_LEVEL"] = params.dlt_debug
        os.environ["EXTRACT__WORKERS"] = "10"
        os.environ["EXTRACT__MAX_PARALLEL_ITEMS"] = "100"
        os.environ["SOURCES__CREDENTIALS__SUBDOMAIN"] = params.sub_domain
        os.environ["SOURCES__CREDENTIALS__EMAIL"] = params.email
        os.environ["SOURCES__CREDENTIALS__TOKEN"] = params.api_token

        # set the dataset and pipeline names
        self.dataset_name = DATASET_NAME
        self.pipeline_name = PIPELINE_NAME
        self.duckdb_file = f"{DUCKDB_TMP_DIR}/{self.pipeline_name}.duckdb"

        # check if the duckdb file exists delete it - especially for the local run
        if os.path.exists(self.duckdb_file):
            os.remove(self.duckdb_file)
        self.pipeline_destination = dlt.destinations.duckdb(self.duckdb_file)

    def _run_dlt_pipeline(self, start_date_iso) -> list:
        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination=self.pipeline_destination,
            dataset_name=self.dataset_name,
            progress="log",
        )
        pipeline = pipeline.run(zendesk_support(start_date_iso), refresh="drop_sources")
        pipeline.raise_on_failed_jobs()

        loaded_tables = []
        for package in pipeline.load_packages:
            jobs = package.jobs.get("completed_jobs", [])
            for job in jobs:
                table = job.job_file_info.table_name
                if not table.startswith("dlt_"):
                    loaded_tables.append(table)

        return loaded_tables

    def _prepare_views(self, loaded_tables):
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
        for view in views:
            # get the schema of the view
            table_meta = self.connection.execute(f"""DESCRIBE {view.name};""").fetchall()
            schema = OrderedDict(
                (c[0], ColumnDefinition(data_types=BaseType(dtype=self.convert_base_types(c[1])))) for c in table_meta)

            # prepare the out table
            out_table = self.create_out_table_definition(f"{view.name}.csv",
                                                         schema=schema,
                                                         primary_key=view.primary_key,
                                                         incremental=True,
                                                         destination=view.name,
                                                         has_header=True,
                                                         )
            # export the view
            logging.info(f"Exporting view {view.name}")
            try:
                export_query = f"""COPY '{view.name}' TO '{out_table.full_path}
                                '(HEADER false, DELIMITER ',', FORCE_QUOTE *)"""
                self.connection.execute(export_query)
            except duckdb.ConversionException as e:
                raise UserException(f"Error during query execution: {e}")

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
        self.connection = duckdb.connect(duck_db_file)


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
