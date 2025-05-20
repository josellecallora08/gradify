import pandas as pd
import os
import re
import json
from dotenv import load_dotenv
from app.interfaces import CallbackHandler
from app.common import AppContext
import requests
from app.common.utilities import delete_file
from typing import Dict
load_dotenv('.env', override=True)

class EvaluateTrainees(CallbackHandler):
    def __init__(self, context: AppContext):
        self.ctx = context
        self.excel_reader = self.ctx.excel_reader
    
    async def download_csv_from_payload(self, payload: Dict) -> str:
        """
        Downloads the attached CSV file from the Lark payload and saves it to ./storage/er/.
        Skips download if file already exists.
        """
        try:
            self.ctx.logger.info("📥 Downloading Excel File")
            file_info = payload["file"][0]
            print(payload)
            file_name = f"data-{payload['uploaded_by'][0]['id']}.csv"
            file_path = os.path.join("storage", "er", file_name)

            if os.path.exists(file_path):
                self.ctx.logger.info(f"📂 File already exists. Skipping download: {file_path}")
                return file_path

            file_token = file_info["file_token"]
            record_id = payload["record_id"]

            # Prepare payload
            download_payload = {
                "file_token": file_token,
                "record_id": record_id
            }

            # Perform download
            await self.ctx.base_manager.adownload(
                payload=download_payload,
                folder_name="storage/er",
                file_name=file_name
            )
            

            self.ctx.logger.info(f"✅ File downloaded successfully: {file_path}")
            return file_path

        except Exception as e:
            self.ctx.logger.error(f"❌ Failed to download file from payload: {e}")
            raise

    async def handler(self, payload: Dict[str, str]):
        self.ctx.logger.info("📝 Starting realization evaluation...")
        try:
            return 1;

        except Exception as e:
            self.ctx.logger.error(f"❌ Error during realization evaluation: {e}")
        
        finally:
            self.ctx.logger.info("✅ Finished realization evaluation.")
