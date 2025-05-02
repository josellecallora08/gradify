from typing import Literal
from app.src.lark import BitableManager


class BubbleDataStore:

    def __init__(self, table_id: str, base_manager: BitableManager):
        self.table_id: str = table_id
        self.base_manager: BitableManager = base_manager

    async def update_status(
        self,
        record_id: str,
        status: Literal["done", "failed", "file deleted", "invalid audio url", "audio_less_than_30_secs", "script error"]
    ):
        try:
            await self.base_manager.update_record_async(
                table_id=self.table_id,
                record_id=record_id,
                fields={
                    "status": status
                }
            )
        except Exception as err:
            raise Exception("BubbleDataStore updating status failed: ", err)

    async def increment_retry(self, record_id: str, count: int):
        try:
            await self.base_manager.update_record_async(
                table_id=self.table_id,
                record_id=record_id,
                fields={
                    "no_of_retries": count + 1
                }
            )
        except Exception as err:
            raise Exception("BubbleDataStore failed to increment retry:", err)
    
    async def get_unprocessed_items(self, filter):
        try:
            response = await self.base_manager.async_get_records(
                self.table_id,
                filter=filter
            )
            return response
        except Exception as err:
            raise Exception("BubbleDataStore failed to get items: ", err)
            

