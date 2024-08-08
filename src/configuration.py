import logging

from pydantic import BaseModel, Field, ValidationError
from keboola.component.exceptions import UserException


class Configuration(BaseModel):
    email: str = Field()
    api_token: str = Field(alias="#api_token")
    sub_domain: str = Field()
    debug: bool = Field(default=False)
    dlt_debug: str = "DEBUG" if debug else "INFO"

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as e:
            error_messages = [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            raise UserException(f"Validation Error: {', '.join(error_messages)}")

        if self.debug:
            logging.debug("Component will run in Debug mode")
