from app.src.lark import BitableManager


class TraineeEvaluatedRecordService:
    def __init__(self, base_manager: BitableManager):
        self.base_manager = base_manager

    async def update_number_of_retries(self, table_id: str, record_id: str, no_of_retries: int):
        try:
            await self.base_manager.update_record_async(
                table_id=table_id,
                record_id=record_id,
                fields={
                    "no_of_retries": no_of_retries + 1
                }
            )
        except Exception as err:
            raise Exception("Error: message=%s, status=cant increment no_of_retries")

    async def done_processing(self, table_id: str, record_id: str):
        """mark current record as done when the worker is done at processing it"""
        try:
            await self.base_manager.update_record_async(
                table_id=table_id,
                record_id=record_id,
                fields={
                    "status": "done"
                }
            )
        except Exception as err:
            raise Exception(f"Error: message=%s, status= updating record failed: %s", err, record_id)