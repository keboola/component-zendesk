import logging
from typing import Iterable, Iterator

import dlt
import pendulum

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
        ("groups", "/api/v2/groups.json", Groups),
        ("group_memberships", "/api/v2/group_memberships.json", GroupMembership),
        ("organizations", "/api/v2/organizations.json", Organizations),
        ("tags", "/api/v2/tags.json", Tags),
        ("ticket_fields", "/api/v2/ticket_fields.json", TicketsFields),
    ]

    @dlt.resource(name="users_raw", parallelized=True, columns=Users, write_disposition="replace")
    def users() -> Iterator[TDataItem]:
        dt = pendulum.from_timestamp(start_date_iso)
        from_date = dt.format('YYYY-MM-DD')

        logging.info(f"Loading users")
        user_pages = zendesk_client.get_pages(
            "/api/v2/users/search.json",
            "users",
            PaginationType.OFFSET,
            params={"query": f"type:user updated>{from_date}"},
        )
        yield from user_pages

    @dlt.resource(name="tickets_raw", parallelized=True, columns=Tickets, write_disposition="replace")
    def ticket_table() -> Iterator[TDataItem]:
        logging.info("Loading tickets")
        ticket_pages = zendesk_client.get_pages(
            "/api/v2/incremental/tickets.json",
            "tickets",
            PaginationType.STREAM,
            params={"include": "metric_sets,comment_count",
                    "start_time": start_date_iso},
        )
        yield from ticket_pages

    @dlt.transformer(name="ticket_comments_raw", parallelized=True, columns=TicketComments)
    def ticket_comments(tickets: Iterator[TDataItem]):
        logging.info("Loading ticket comments")
        for ticket in tickets:
            # try if page not found write to log
            try:
                comment_pages = zendesk_client.get_pages(
                    f"/api/v2/tickets/{ticket['id']}/comments.json",
                    "comments",
                    PaginationType.CURSOR,
                )
                for comments in comment_pages:
                    yield [dict(ticket_id=ticket['id'], **i) for i in comments]
            except Exception as e:
                logging.warning(f"Ticket {ticket['id']} comments not found {e}")

    @dlt.transformer(name="ticket_audits_raw", parallelized=True, columns=TicketAudits)
    def ticket_audits(tickets: Iterator[TDataItem]):
        logging.info("Loading ticket audits")
        for ticket in tickets:
            try:
                audit_pages = zendesk_client.get_pages(
                    f"/api/v2/tickets/{ticket['id']}/audits.json",
                    "audits",
                    PaginationType.CURSOR,
                )
                for audits in audit_pages:
                    yield audits
            except Exception as e:
                logging.warning(f"Ticket {ticket['id']} audits not found {e}")

    # Authenticate
    zendesk_client = ZendeskAPIClient(credentials)

    # loading base tables
    resource_list = [
        users,
        ticket_table,
        ticket_table | ticket_comments,
        ticket_table | ticket_audits
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
    logging.info(f"Loading {data_key}")
    pages = zendesk_client.get_pages(
        endpoint_url,
        data_key,
        PaginationType.CURSOR,
    )
    yield from pages
