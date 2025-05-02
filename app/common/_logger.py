from app.src.lark import BitableManager
import os

class Logger:
    def __init__(self, base_manager: BitableManager):
        self.base_manager = base_manager
        self.logs_table_id = os.getenv('LOGS_TABLE_ID')
        self.environment = os.getenv('ENV')

    async def create_record_async(self, message: str, error_type: str):
        try:
            if self.environment == 'production':
                environment = 'production'
            else:
                environment = 'development'

            await self.base_manager.create_record_async(
                table_id=self.logs_table_id,
                fields={
                    "message": str(message),
                    "error_type": str(error_type),
                    "environment": environment
                }
            )
        except Exception as err:
            print("Failed to update logs: ", err)