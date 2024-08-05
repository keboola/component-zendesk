"""Zendesk source settings and constants"""
from dlt.common import pendulum

PAGE_SIZE = 100
INCREMENTAL_PAGE_SIZE = 1000
DEFAULT_START_DATE = pendulum.datetime(year=2000, month=1, day=1)

