import logging
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, computed_field
from keboola.component.exceptions import UserException


class Authentication(BaseModel):
    email: str = Field()
    api_token: str = Field(alias="#api_token")
    sub_domain: str = Field()


class SyncOptions(BaseModel):
    sync_mode: str

    @computed_field
    def is_incremental(self) -> bool:
        return self.sync_mode == "incremental_sync"


class Destination(BaseModel):
    load_type: str
    destination_bucket: str = Field(default=None)

    @computed_field
    def is_incremental_load_type(self) -> bool:
        return self.load_type == "incremental_load"


class AvailableDetails(BaseModel):
    ticket_comments_raw: bool
    ticket_audits_raw: bool


class Configuration(BaseModel):
    authentication: Authentication
    sync_options: SyncOptions
    destination: Destination
    available_details: AvailableDetails
    debug: bool = Field(default=False)

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            raise UserException(f"Validation Error: {', '.join(error_messages)}")

        if self.debug:
            logging.debug("Component will run in Debug mode")
