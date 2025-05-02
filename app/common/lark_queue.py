from app.src.lark import BitableManager
from lark_oapi.api.bitable.v1 import AppTableRecord
from typing import List
from dataclasses import dataclass

@dataclass
class LarkQueue:
    base_manager: BitableManager
    bitable_table_id: str
    version: str
    environment: str

    async def get_items(self, server_task: str) -> List[AppTableRecord]:
        # query = f"AND(AND(AND(OR(CurrentValue.[status] = \"\", CurrentValue.[status] = \"failed\"), CurrentValue.[no_of_retries] <= 3), CurrentValue.[version] = \"{self.version}\"), CurrentValue.[environment] = \"{self.environment.upper()}\")"
        query = f"AND(AND(AND(CurrentValue.[version] = \"{self.version}\", CurrentValue.[environment] = \"{self.environment.upper()}\"), AND(CurrentValue.[status] = \"\", CurrentValue.[no_of_retries] <= 3)), CurrentValue.[assessment_type] = \"{server_task}\")"
        records = await self.base_manager.async_get_records(
            table_id=self.bitable_table_id,
            filter=query
        )
        print(self.bitable_table_id)
        
        return records
