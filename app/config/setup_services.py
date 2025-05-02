from app.src.lark import Lark, BitableManager, FileManager
from app.services import ExcelReader, GroqService, APIManager
from app.config.config import config, groq_api_keys_manager
from typing import Dict
lark_client = Lark(
    app_id=config.APP_ID,
    app_secret=config.APP_SECRET,
    debug=True
)

base_manager = BitableManager(
    lark_client=lark_client,
    bitable_token=config.BITABLE_TOKEN,
    bitable_id=config.UNPROCESSED_TABLE_ID
)

file_manager = FileManager(
    lark_client=lark_client,
    bitable_token=config.BITABLE_TOKEN
)

excel_reader = ExcelReader(data_folder="storage/er")

groq_service = GroqService(api_manager=groq_api_keys_manager)


