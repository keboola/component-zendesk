from datetime import date
from typing import Iterable, Iterator

import dlt

from dlt.common.time import ensure_pendulum_datetime
from dlt.common.typing import TDataItem
from dlt.sources import DltResource

from .helpers.credentials import TZendeskCredentials
from .helpers.api_client import ZendeskAPIClient, PaginationType

from .settings import DEFAULT_START_DATE

from .zendesk_objects import *


@dlt.source(max_table_nesting=2)
def zendesk_support(credentials: TZendeskCredentials = dlt.secrets.value,
                    start_date: date = DEFAULT_START_DATE) -> Iterable[DltResource]:
    """
    Retrieves data from Zendesk Support for tickets, users, brands, organizations, and groups.

    `start_date` argument can be used on its own or together with `end_date`. When both are provided
    data is limited to items updated in that time range.
    The range is "half-open", meaning elements equal and higher than `start_date` and elements lower than `end_date`
    are included.

    Args:
        credentials: The credentials for authentication. Defaults to the value in the `dlt.secrets` object.
        start_date: The start time of the range for which to load. Defaults to January 1st 2000.

    Returns:
        Sequence[DltResource]: Multiple dlt resources.
    """

    # Tuples of (Resource name, endpoint URL, data_key, supports pagination)
    # data_key is the key which data list is nested under in responses
    # if the data key is None it is assumed to be the same as the resource name
    # The last element of the tuple says if endpoint supports cursor pagination
    supported_endpoints = [
        ("users", "/api/v2/users.json", Users, ["id"], True),
        ("groups", "/api/v2/groups.json", Groups, None, True),
        ("group_memberships", "/api/v2/group_memberships.json", None, None, True),
        ("organizations", "/api/v2/organizations.json", Organizations, None, True),
        ("tags", "/api/v2/tags.json", None, None, True),
        ("ticket_fields", "/api/v2/ticket_fields.json", TicketsFields, None, True),
    ]

    @dlt.resource(name="tickets", write_disposition="replace", parallelized=True, primary_key=["id"], columns=Tickets)
    def ticket_table() -> Iterator[TDataItem]:
        """
        Resource for tickets table. Uses DLT state to handle column renaming of custom fields to prevent changing
        the names of said columns. This resource uses pagination,loading and side loading to make API calls
        more efficient.

        Yields:
            TDataItem: Dictionary containing the ticket data.
        """
        ticket_pages = zendesk_client.get_pages(
            "/api/v2/incremental/tickets.json",
            "tickets",
            PaginationType.STREAM,
            params={"include": "metric_sets,comment_count", "start_time": start_date_obj.int_timestamp},
        )
        for page in ticket_pages:
            yield page

    @dlt.transformer(write_disposition="replace", parallelized=True, columns=TicketComments)
    def ticket_comments(ticket_table: Iterator[TDataItem]) -> Iterator[TDataItem]:
        for ticket in ticket_table:
            comment_pages = zendesk_client.get_pages(
                f"/api/v2/tickets/{ticket['id']}/comments.json",
                "comments",
                PaginationType.CURSOR,
            )
            for comments in comment_pages:
                yield [dict(ticket_id=ticket['id'], **i) for i in comments]

    @dlt.transformer(write_disposition="replace", parallelized=True, columns=TicketAudits)
    def ticket_audits(ticket_table: Iterator[TDataItem]) -> Iterator[TDataItem]:
        for ticket in ticket_table:
            audit_pages = zendesk_client.get_pages(
                f"/api/v2/tickets/{ticket['id']}/audits.json",
                "audits",
                PaginationType.CURSOR,
            )
            for audits in audit_pages:
                yield audits

    start_date_obj = ensure_pendulum_datetime(start_date)

    # Authenticate
    zendesk_client = ZendeskAPIClient(credentials)

    # loading base tables
    resource_list = [
        ticket_table(),
        ticket_table() | ticket_comments,
        ticket_table() | ticket_audits
    ]
    # other tables to be loaded
    for resource, endpoint_url, columns, primary_key, cursor_paginated in list(supported_endpoints):
        resource_list.append(
            dlt.resource(
                basic_resource(
                    zendesk_client, endpoint_url, resource, cursor_paginated
                ),
                name=resource,
                primary_key=primary_key,
                columns=columns,
                write_disposition="replace",
                parallelized=True,
            )
        )
    return resource_list


def basic_resource(zendesk_client: ZendeskAPIClient, endpoint_url: str, data_key: str, cursor_paginated: bool, ) -> \
        Iterator[TDataItem]:
    pages = zendesk_client.get_pages(
        endpoint_url,
        data_key,
        PaginationType.CURSOR if cursor_paginated else PaginationType.OFFSET,
    )
    yield from pages
