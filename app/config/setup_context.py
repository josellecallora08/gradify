from app.common import AppContext, LarkQueue, TaskQueue
from .config import config
from .setup_services import base_manager, file_manager, excel_reader, groq_service
import logging
from .setup_constants import base_constants
from .setup_stores import stores
context = AppContext(
    base_manager=base_manager,
    file_manager=file_manager,
    excel_reader=excel_reader,
    lark_queue=LarkQueue(
        base_manager=base_manager,
        bitable_table_id=base_constants.UNPROCESSED_TABLE_ID,
        environment=config.ENVIRONMENT,
        version=config.VERSION,
    ),
    task_queue=TaskQueue(),
    stores=stores,
    logger=logging.getLogger(),
    groq_service=groq_service,
    environment=config.ENVIRONMENT,
    version=config.VERSION
)
