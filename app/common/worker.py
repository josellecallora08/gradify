import os
from dataclasses import dataclass, asdict
from datetime import datetime
from app.common import (DataTransformer,
                        AppContext)


@dataclass
class Worker:
    """Worker is responsible for processing applicant submission"""

    def __init__(self, ctx: AppContext, server_task: str):
        self._ctx = ctx
        self.server_task = server_task

    def create_storage_folders(self):
        """Create storage folder when running worker.py"""
        temporary_storage_dir = os.path.join('storage', 'temporary_storage')
        if not os.path.exists(temporary_storage_dir):
            os.makedirs(temporary_storage_dir)

    async def sync(self):
        """Synchronize items from lark to TaskQueue"""
        # Get the current date and time
        now = datetime.now()

        # Format the date and time
        formatted_time = now.strftime("%A at %I:%M %p")

        self._ctx.logger.info('🔄 syncing from lark at %s', formatted_time)

        records = await self._ctx.lark_queue.get_items(self.server_task)

        if len(records) == 0:
            return

        transformed_records = DataTransformer.convert_raw_lark_record_to_dict(
            records,
            [
                "record_id",
                "version",
                "assessment_type",
                "environment",
                "file",
                "download_url",
                "status",
                "date",
                "uploaded_by"
            ]
        )
        self._ctx.task_queue.enqueue_many(transformed_records)
