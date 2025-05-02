import os
from ._base_constants import BaseConstants

base_constants = BaseConstants(
    SR_GROUP_CHAT_ID=os.getenv("SR_GROUP_CHAT_ID"),
    UNPROCESSED_TABLE_ID=os.getenv("UNPROCESSED_TABLE_ID"),
)