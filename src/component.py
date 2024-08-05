import os
import time
import logging
from collections import OrderedDict
from typing import Any

import dlt
from duckdb import duckdb
from keboola.component.base import ComponentBase
from keboola.component.dao import ColumnDefinition, BaseType, SupportedDataTypes
from keboola.component.exceptions import UserException

from configuration import Configuration

from dlt_zendesk_client import zendesk_support


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

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

        # check for missing configuration parameters
        params = Configuration(**self.configuration.parameters)

        dlt_tmp_dir = "/tmp/.dlt"
        os.makedirs(dlt_tmp_dir, exist_ok=True)
        os.environ["RUNTIME__DLT_DATA_DIR"] = dlt_tmp_dir
        os.environ["RUNTIME__DLTHUB_TELEMETRY"] = "false"
        os.environ["RUNTIME__LOG_LEVEL"] = "DEBUG" if params.debug else "INFO"
        os.environ["SOURCES__CREDENTIALS__SUBDOMAIN"] = params.sub_domain
        os.environ["SOURCES__CREDENTIALS__EMAIL"] = params.email
        os.environ["SOURCES__CREDENTIALS__TOKEN"] = params.api_token

        self.dataset_name = "zendesk_data"
        self.pipeline_name = "dlt_zendesk_pipeline"
        self.pipeline_destination = dlt.destinations.duckdb(f"./{self.pipeline_name}.duckdb")

        start = time.time()
        pipeline = self.run_zendesk_pipeline()
        end = time.time()
        print(f"Time taken: {end - start}")
        pipeline.raise_on_failed_jobs()

        self._init_connection(duck_db_file=self.pipeline_destination.config_params.get('credentials'))

        out_tables = self._get_tables(database=self.dataset_name)

        for table in out_tables:

            table_meta = self.connection.execute(f"""DESCRIBE TABLE '{table}';""").fetchall()
            schema = OrderedDict(
                (c[0], ColumnDefinition(data_types=BaseType(dtype=self.convert_base_types(c[1])))) for c in table_meta
                if not str(c[0]).startswith('_dlt'))

            # primary_key = [c[0] for c in table_meta if c[3] == 'PRI']
            out_table = self.create_out_table_definition(f"{table}.csv",
                                                         schema=schema,
                                                         # TODO primary_key
                                                         primary_key=[],
                                                         # TODO incremental
                                                         incremental=False,
                                                         destination=table,
                                                         )

            try:
                columns = ",".join([f"\"{c[0]}\"" for c in schema.items()])
                export_query = f'''COPY (SELECT {columns} FROM "{table}") TO "{out_table.full_path}"
                                                            (HEADER, DELIMITER ',', FORCE_QUOTE *)'''
                self.connection.execute(export_query)
            except duckdb.ConversionException as e:
                raise UserException(f"Error during query execution: {e}")

            self.write_manifest(out_table)

    def run_zendesk_pipeline(self) -> Any:
        """
        Loads all possible tables for Zendesk Support
        """
        pipeline = dlt.pipeline(
            pipeline_name=self.pipeline_name,
            destination=self.pipeline_destination,
            dataset_name=self.dataset_name,
            progress="log",
        )

        return pipeline.run(zendesk_support(), refresh="drop_sources")
        # return pipeline.run(zendesk_support().with_resources("tickets"))

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

    def _get_tables(self, database):
        all_tables = self.connection.sql(f"USE {database}; SHOW TABLES;").fetchall()
        return [t[0] for t in all_tables if not str(t[0]).startswith("_dlt")]


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
