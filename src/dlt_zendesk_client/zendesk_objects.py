from typing import Optional, ClassVar

from dlt.common.libs.pydantic import BaseModel, DltConfig
from pydantic import Field, field_validator, model_serializer

'''
class Thumbnails(BaseModel):
    content_type: Optional[str]
    content_url: Optional[str]
    id: Optional[int]
    name: Optional[str]
    size: Optional[int]


class Photo(BaseModel):
    id: int
    file_name: Optional[str] = Field(alias='name')
    content_url: Optional[str]
    content_type: Optional[str]
    size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    inline: Optional[str]
    thumbnails: Thumbnails


class TicketsFields(BaseModel):
    id: int
    type: Optional[str]
    title: Optional[str]
    active: Optional[str]
    tag: Optional[str]


class SatisfactionRating(BaseModel):
    id: Optional[int]
    score: Optional[str]
    comment: Optional[str]


class TicketsMetric(BaseModel):
    id: int
    ticket_id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    group_stations: Optional[int]
    assignee_stations: Optional[int]
    reopens: Optional[int]
    replies: Optional[int]
    assignee_updated_at: Optional[str]
    requester_updated_at: Optional[str]
    status_updated_at: Optional[str]
    initially_assigned_at: Optional[str]
    assigned_at: Optional[str]
    solved_at: Optional[str]
    latest_comment_added_at: Optional[str]
    reply_time_in_minutes_calendar: Optional[int] = Field(alias='reply_time_in_minutes.calendar',
                                                          validation_alias=AliasPath('reply_time_in_minutes',
                                                                                     'calendar'))
    reply_time_in_minutes_business: Optional[int] = Field(alias='reply_time_in_minutes.business',
                                                          validation_alias=AliasPath('reply_time_in_minutes',
                                                                                     'business'))
    first_resolution_time_in_minutes_calendar: Optional[int] = Field(alias='first_resolution_time_in_minutes.calendar',
                                                                     validation_alias=AliasPath(
                                                                         'first_resolution_time_in_minutes',
                                                                         'calendar'))
    first_resolution_time_in_minutes_business: Optional[int] = Field(alias='first_resolution_time_in_minutes.business',
                                                                     validation_alias=AliasPath(
                                                                         'first_resolution_time_in_minutes',
                                                                         'business'))
    full_resolution_time_in_minutes_calendar: Optional[int] = Field(alias='full_resolution_time_in_minutes.calendar',
                                                                    validation_alias=AliasPath(
                                                                        'full_resolution_time_in_minutes',
                                                                        'calendar'))
    full_resolution_time_in_minutes_business: Optional[int] = Field(alias='full_resolution_time_in_minutes.business',
                                                                    validation_alias=AliasPath(
                                                                        'full_resolution_time_in_minutes',
                                                                        'business'))
    agent_wait_time_in_minutes_calendar: Optional[int] = Field(alias='agent_wait_time_in_minutes.calendar',
                                                               validation_alias=AliasPath('agent_wait_time_in_minutes',
                                                                                          'calendar'))
    agent_wait_time_in_minutes_business: Optional[int] = Field(alias='agent_wait_time_in_minutes.business',
                                                               validation_alias=AliasPath('agent_wait_time_in_minutes',
                                                                                          'business'))
    requester_wait_time_in_minutes_calendar: Optional[int] = Field(alias='requester_wait_time_in_minutes.calendar',
                                                                   validation_alias=AliasPath(
                                                                       'requester_wait_time_in_minutes', 'calendar'))
    requester_wait_time_in_minutes_business: Optional[int] = Field(alias='requester_wait_time_in_minutes.business',
                                                                   validation_alias=AliasPath(
                                                                       'requester_wait_time_in_minutes', 'business'))
    on_hold_time_in_minutes_calendar: Optional[int] = Field(alias='on_hold_time_in_minutes.calendar',
                                                            validation_alias=AliasPath('on_hold_time_in_minutes',
                                                                                       'calendar'))
    on_hold_time_in_minutes_business: Optional[int] = Field(alias='on_hold_time_in_minutes.business',
                                                            validation_alias=AliasPath('on_hold_time_in_minutes',
                                                                                       'business'))


class Tags(BaseModel):
    forceType: Optional[str]
    Optional[str]: Optional[str]


class UserFields(BaseModel):
    user_date: Optional[str]
    user_decimal: Optional[float]
    user_dropdown: Optional[str]


class Users(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    url: Optional[str]
    deleted: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]
    time_zone: Optional[str]
    phone: Optional[str]
    photo: Photo
    locale_id: Optional[int]
    locale: Optional[str]
    organization_id: Optional[int]
    role: Optional[str]
    role_type: Optional[int]
    verified: Optional[str]
    external_id: Optional[str]
    alias: Optional[str]
    active: Optional[bool]
    shared: Optional[bool]
    shared_agent: Optional[bool]
    last_login_at: Optional[str]
    two_factor_auth_enabled: Optional[str]
    signature: Optional[str]
    details: Optional[str]
    notes: Optional[str]
    custom_role_id: Optional[int]
    moderator: Optional[bool]
    ticket_restriction: Optional[str]
    only_private_comments: Optional[bool]
    restricted_agent: Optional[bool]
    suspended: Optional[bool]
    chat_only: Optional[bool]
    user_fields: UserFields
    tags: Tags


class Groups(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    deleted: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class DomainNames(BaseModel):
    domain: Optional[str] = Field(alias='.')


class Organizations(BaseModel):
    id: int
    name: Optional[str]
    url: Optional[str]
    shared_tickets: Optional[str]
    shared_comments: Optional[str]
    external_id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    domain_names: DomainNames
    details: Optional[str]
    notes: Optional[str]
    group_id: Optional[str]
    tags: Optional[list[str]]


'''


class TicketsFieldsValues(BaseModel):
    id: Optional[int]
    value: Optional[str]


class Tickets(BaseModel):
    id: int = None
    url: Optional[str]
    external_id: Optional[int]
    type: Optional[str]
    subject: Optional[str]
    priority: Optional[str]
    status: Optional[str]
    recipient: Optional[str]
    requester_id: Optional[int]
    submitter_id: Optional[int]
    assignee_id: Optional[int]
    organization_id: Optional[int]
    group_id: Optional[int]
    forum_topic_id: Optional[int]
    problem_id: Optional[int]
    has_incidents: Optional[bool]
    due_at: Optional[str]
    via: Optional[object]
    custom_fields: list[TicketsFieldsValues] = []
    # satisfaction_rating: Optional[SatisfactionRating]
    ticket_form_id: Optional[int]
    brand_id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    tags: Optional[list[str]]
    # metric_set: Optional[TicketsMetric]

    dlt_config: ClassVar[DltConfig] = {"skip_complex_types": True}

