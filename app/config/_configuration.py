from typing import Literal, Union
from pydantic import BaseModel
from os import getenv


class Configuration(BaseModel):
    APP_ID: Union[str, None] = getenv('APP_ID')
    APP_SECRET: Union[str, None] = getenv('APP_SECRET')
    UNPROCESSED_TABLE_ID: Union[str, None] = getenv('UNPROCESSED_TABLE_ID')
    BITABLE_TOKEN: Union[str, None] = getenv('BITABLE_TOKEN')
    VERSION: Union[str, None] = getenv('VERSION')
    ENVIRONMENT: Union[str, None] = getenv('ENV')