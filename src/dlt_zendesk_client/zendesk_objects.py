from typing import Optional, ClassVar

from dlt.common.libs.pydantic import BaseModel, DltConfig
from pydantic import Field, AliasPath


class Thumbnails(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    size: Optional[int] = Field(default=None)
    content_type: Optional[str] = Field(default=None)
    content_url: Optional[str] = Field(default=None)


class Photo(BaseModel):
    id: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None)
    content_url: Optional[str] = Field(default=None)
    content_type: Optional[str] = Field(default=None)
    size: Optional[int] = Field(default=None)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    thumbnails: Optional[list[Thumbnails]]


class TicketsFields(BaseModel):
    id: Optional[int] = Field(default=None)
    type: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    active: Optional[bool] = Field(default=None)
    tag: Optional[str] = Field(default=None)


class SatisfactionRating(BaseModel):
    id: Optional[int] = Field(default=None)
    score: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default=None)


class TicketsMetric(BaseModel):
    id: Optional[int] = Field(default=None)
    ticket_id: Optional[int] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    group_stations: Optional[int] = Field(default=None)
    assignee_stations: Optional[int] = Field(default=None)
    reopens: Optional[int] = Field(default=None)
    replies: Optional[int] = Field(default=None)
    assignee_updated_at: Optional[str] = Field(default=None)
    requester_updated_at: Optional[str] = Field(default=None)
    status_updated_at: Optional[str] = Field(default=None)
    initially_assigned_at: Optional[str] = Field(default=None)
    assigned_at: Optional[str] = Field(default=None)
    solved_at: Optional[str] = Field(default=None)
    latest_comment_added_at: Optional[str] = Field(default=None)
    reply_time_in_minutes_calendar: Optional[int] = Field(default=None, alias='reply_time_in_minutes.calendar',
                                                          validation_alias=AliasPath('reply_time_in_minutes',
                                                                                     'calendar'))
    reply_time_in_minutes_business: Optional[int] = Field(default=None, alias='reply_time_in_minutes.business',
                                                          validation_alias=AliasPath('reply_time_in_minutes',
                                                                                     'business'))
    first_resolution_time_in_minutes_calendar: Optional[int] = Field(default=None,
                                                                     alias='first_resolution_time_in_minutes.calendar',
                                                                     validation_alias=AliasPath(
                                                                         'first_resolution_time_in_minutes',
                                                                         'calendar'))
    first_resolution_time_in_minutes_business: Optional[int] = Field(default=None,
                                                                     alias='first_resolution_time_in_minutes.business',
                                                                     validation_alias=AliasPath(
                                                                         'first_resolution_time_in_minutes',
                                                                         'business'))
    full_resolution_time_in_minutes_calendar: Optional[int] = Field(default=None,
                                                                    alias='full_resolution_time_in_minutes.calendar',
                                                                    validation_alias=AliasPath(
                                                                        'full_resolution_time_in_minutes',
                                                                        'calendar'))
    full_resolution_time_in_minutes_business: Optional[int] = Field(default=None,
                                                                    alias='full_resolution_time_in_minutes.business',
                                                                    validation_alias=AliasPath(
                                                                        'full_resolution_time_in_minutes',
                                                                        'business'))
    agent_wait_time_in_minutes_calendar: Optional[int] = Field(default=None,
                                                               alias='agent_wait_time_in_minutes.calendar',
                                                               validation_alias=AliasPath('agent_wait_time_in_minutes',
                                                                                          'calendar'))
    agent_wait_time_in_minutes_business: Optional[int] = Field(default=None,
                                                               alias='agent_wait_time_in_minutes.business',
                                                               validation_alias=AliasPath('agent_wait_time_in_minutes',
                                                                                          'business'))
    requester_wait_time_in_minutes_calendar: Optional[int] = Field(default=None,
                                                                   alias='requester_wait_time_in_minutes.calendar',
                                                                   validation_alias=AliasPath(
                                                                       'requester_wait_time_in_minutes', 'calendar'))
    requester_wait_time_in_minutes_business: Optional[int] = Field(default=None,
                                                                   alias='requester_wait_time_in_minutes.business',
                                                                   validation_alias=AliasPath(
                                                                       'requester_wait_time_in_minutes', 'business'))
    on_hold_time_in_minutes_calendar: Optional[int] = Field(default=None, alias='on_hold_time_in_minutes.calendar',
                                                            validation_alias=AliasPath('on_hold_time_in_minutes',
                                                                                       'calendar'))
    on_hold_time_in_minutes_business: Optional[int] = Field(default=None, alias='on_hold_time_in_minutes.business',
                                                            validation_alias=AliasPath('on_hold_time_in_minutes',
                                                                                       'business'))


class UserFields(BaseModel):
    user_date: Optional[str] = Field(default=None)
    user_decimal: Optional[float] = Field(default=None)
    user_dropdown: Optional[str] = Field(default=None)


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
    photo: Optional[Photo]
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
    two_factor_auth_enabled: Optional[str] = Field(default=None)
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
    user_fields: Optional[UserFields]
    tags: Optional[list] = Field(default=None)


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
    external_id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    domain_names: Optional[list]
    details: Optional[str]
    notes: Optional[str]
    group_id: Optional[int]
    tags: Optional[list[str]]


class TicketsFieldsValues(BaseModel):
    id: Optional[int]
    value: Optional[str]


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
    via: Optional[object] = Field(default=None)
    custom_fields: list[TicketsFieldsValues] = Field(default=None)
    satisfaction_rating: Optional[SatisfactionRating]
    ticket_form_id: Optional[int] = Field(default=None)
    brand_id: Optional[int] = Field(default=None)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    tags: Optional[list]
    metric_set: Optional[TicketsMetric]

    # dlt_config: ClassVar[DltConfig] = {"skip_complex_types": True}


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

