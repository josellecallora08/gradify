from pydantic import BaseModel


class BaseConstants(BaseModel):
    SR_GROUP_CHAT_ID: str
    UNPROCESSED_TABLE_ID: str