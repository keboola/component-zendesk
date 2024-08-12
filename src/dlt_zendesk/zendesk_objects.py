from typing import Optional

from dlt.common.libs.pydantic import BaseModel
from pydantic import Field


class Tags(BaseModel):
    name: Optional[str] = Field(default=None)
    count: Optional[int] = Field(default=None)


class TicketsFields(BaseModel):
    id: Optional[int]
    type: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    tag: Optional[str] = Field(default=None)


class Users(BaseModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    deleted: Optional[bool] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    time_zone: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    photo: Optional[object] = Field(default={})
    locale_id: Optional[int] = Field(default=None)
    locale: Optional[str] = Field(default=None)
    organization_id: Optional[int] = Field(default=None)
    role: Optional[str] = Field(default=None)
    role_type: Optional[int] = Field(default=None)
    verified: Optional[bool] = Field(default=None)
    external_id: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    shared: Optional[bool] = Field(default=None)
    shared_agent: Optional[bool] = Field(default=None)
    last_login_at: Optional[str] = Field(default=None)
    two_factor_auth_enabled: Optional[bool] = Field(default=None)
    signature: Optional[str] = Field(default=None)
    details: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)
    custom_role_id: Optional[int] = Field(default=None)
    moderator: Optional[bool] = Field(default=None)
    ticket_restriction: Optional[str] = Field(default=None)
    only_private_comments: Optional[bool] = Field(default=None)
    restricted_agent: Optional[bool] = Field(default=None)
    suspended: Optional[bool] = Field(default=None)
    chat_only: Optional[bool] = Field(default=None)
    user_fields: Optional[object] = Field(default={})
    tags: Optional[list] = Field(default=[])


class GroupMembership(BaseModel):
    id: int
    default: Optional[bool]
    group_id: Optional[int]
    user_id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]


class Groups(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    deleted: Optional[bool] = Field(default=None)
    created_at: Optional[str]
    updated_at: Optional[str]


class Organizations(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    organization_fields: Optional[object]
    shared_tickets: Optional[bool]
    shared_comments: Optional[bool]
    external_id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    domain_names: Optional[list] = Field(default=[])
    details: Optional[str]
    notes: Optional[str]
    group_id: Optional[int]
    tags: Optional[list[str]]


class Tickets(BaseModel):
    id: int
    url: Optional[str] = Field(default=None)
    external_id: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None)
    subject: Optional[str] = Field(default=None)
    priority: Optional[str] = Field(default=None)
    status: Optional[str] = Field(default=None)
    recipient: Optional[str] = Field(default=None)
    requester_id: Optional[int] = Field(default=None)
    submitter_id: Optional[int] = Field(default=None)
    assignee_id: Optional[int] = Field(default=None)
    organization_id: Optional[int] = Field(default=None)
    group_id: Optional[int] = Field(default=None)
    forum_topic_id: Optional[int] = Field(default=None)
    problem_id: Optional[int] = Field(default=None)
    has_incidents: Optional[bool] = Field(default=None)
    due_at: Optional[str] = Field(default=None)
    via: Optional[object] = Field(default={})
    custom_fields: Optional[list[object]] = Field(default=[])
    satisfaction_rating: Optional[object] = Field(default={})
    ticket_form_id: Optional[int] = Field(default=None)
    brand_id: Optional[int] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    tags: Optional[list] = Field(default=[])
    metric_set: Optional[object] = Field(default={})


class TicketAudits(BaseModel):
    id: int
    ticket_id: int
    events: Optional[list[object]]
    author_id: Optional[int] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    metadata: Optional[object]
    via: Optional[object]


class TicketComments(BaseModel):
    id: int
    ticket_id: int
    audit_id: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None)
    author_id: Optional[int] = Field(default=None)
    body: Optional[str] = Field(default=None)
    html_body: Optional[str] = Field(default=None)
    plain_body: Optional[str] = Field(default=None)
    public: Optional[bool] = Field(default=None)
    attachments: Optional[list[object]] = Field(default=None)
    via: Optional[object] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    uploads: Optional[list[object]] = Field(default=None)
    metadata: Optional[object] = Field(default=None)
