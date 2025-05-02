import logging
import os
from app.services import ExcelReader, GroqService
from app.src.lark import BitableManager, FileManager
from app.common import TaskQueue , LarkQueue
from app.stores import Stores

class AppContext:
    def __init__(
        self,
        base_manager: BitableManager,
        file_manager: FileManager,
        excel_reader: ExcelReader,
        lark_queue: LarkQueue,
        task_queue: TaskQueue,
        stores: Stores,
        logger: logging.Logger,
        groq_service: GroqService,
        version: str = os.getenv('VERSION'),
        environment: str = os.getenv('ENV')
    ):
        self.base_manager = base_manager
        self.file_manager = file_manager
        self.excel_reader = excel_reader
        self.lark_queue = lark_queue
        self.task_queue = task_queue
        self.stores = stores
        self.logger = logger
        self.groq_serivce = groq_service
        self.version = version
        self.environment = environment