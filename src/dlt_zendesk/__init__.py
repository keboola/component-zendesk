from typing import Iterable, Iterator

import dlt

from dlt.common.typing import TDataItem
from dlt.sources import DltResource

from .helpers.credentials import TZendeskCredentials
from .helpers.api_client import ZendeskAPIClient, PaginationType

from .zendesk_objects import (Tags, Tickets, TicketComments, TicketAudits, Users, Groups, GroupMembership,
                              Organizations,
                              TicketsFields)


@dlt.source(max_table_nesting=0)
def zendesk_support(start_date_iso: int, credentials: TZendeskCredentials = dlt.secrets.value) \
        -> Iterable[DltResource]:
    supported_endpoints = [
        ("users", "/api/v2/users.json", Users),
        ("groups", "/api/v2/groups.json", Groups),
        ("group_memberships", "/api/v2/group_memberships.json", GroupMembership),
        ("organizations", "/api/v2/organizations.json", Organizations),
        ("tags", "/api/v2/tags.json", Tags),
        ("ticket_fields", "/api/v2/ticket_fields.json", TicketsFields),
    ]

    def ticket_table() -> Iterator[TDataItem]:
        ticket_pages = zendesk_client.get_pages(
            "/api/v2/incremental/tickets.json",
            "tickets",
            PaginationType.STREAM,
            params={"include": "metric_sets,comment_count",
                    "start_time": start_date_iso},
        )
        for page in ticket_pages:
            yield page

    def ticket_comments(tickets: Iterator[TDataItem]) -> Iterator[TDataItem]:
        for ticket in tickets:
            comment_pages = zendesk_client.get_pages(
                f"/api/v2/tickets/{ticket['id']}/comments.json",
                "comments",
                PaginationType.CURSOR,
            )
            for comments in comment_pages:
                yield [dict(ticket_id=ticket['id'], **i) for i in comments]

    def ticket_audits(tickets: Iterator[TDataItem]) -> Iterator[TDataItem]:
        for ticket in tickets:
            audit_pages = zendesk_client.get_pages(
                f"/api/v2/tickets/{ticket['id']}/audits.json",
                "audits",
                PaginationType.CURSOR,
            )
            for audits in audit_pages:
                yield audits

    # Authenticate
    zendesk_client = ZendeskAPIClient(credentials)

    # loading base tables
    resource_list = [
        dlt.resource(ticket_table(), name="tickets_raw", parallelized=True, columns=Tickets,
                     write_disposition="replace"),
        ticket_table() | dlt.transformer(ticket_comments, name="ticket_comments_raw", parallelized=True,
                                         columns=TicketComments),
        ticket_table() | dlt.transformer(ticket_audits, name="ticket_audits_raw", parallelized=True,
                                         columns=TicketAudits)
    ]
    # other tables to be loaded
    for resource, endpoint_url, columns in list(supported_endpoints):
        resource_list.append(
            dlt.resource(_basic_resource(zendesk_client, endpoint_url, resource), name=f"{resource}_raw",
                         columns=columns,
                         parallelized=True, )
        )
    return resource_list


def _basic_resource(zendesk_client: ZendeskAPIClient, endpoint_url: str, data_key: str) -> \
        Iterator[TDataItem]:
    pages = zendesk_client.get_pages(
        endpoint_url,
        data_key,
        PaginationType.CURSOR,
    )
    yield from pages
