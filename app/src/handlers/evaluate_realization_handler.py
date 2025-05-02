import pandas as pd
import os
import json
from dotenv import load_dotenv
from app.interfaces import CallbackHandler
from app.common import AppContext
import requests
from app.common.utilities import delete_file
from typing import Dict
load_dotenv('.env', override=True)

class EvaluateRealization(CallbackHandler):
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
            file_name = f"data-{payload['uploaded_by']['id']}.csv"
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
            file_path = await self.ctx.base_manager.adownload(
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
            # ✅ Step 1: Download if needed
            file_path = await self.download_csv_from_payload(payload=payload)

            names = self.excel_reader.clean_and_process_file(ctx=self.ctx)
            # ✅ Step 3: Get cleaned data
            content = self.excel_reader.get_all_data()

            # ✅ Step 4: Loop through all rows
            if content is not None:
                for index, row in content.iterrows():
                    self.ctx.logger.info(f"➡️ Row {index}: {row.to_dict()}")
                    # Example: Access individual fields
                    email = row.get("Email", "")
                    topic, realization = row.get("Result", "").split(',')
                    print(topic)
                    print(realization)
                    with open("data/prompt.md", "r", encoding='utf-8') as f:
                        template = f.read()

                    prompt = template.replace("{{topic}}", topic.split(':')[1]).replace('{{realization}}', realization.split(':')[1])   
                    
                    evaluate = await self.ctx.groq_serivce.chat(prompt=prompt)  
                    cleaned = evaluate.replace('```json', '').replace('```','')
                    parsed = json.loads(cleaned)

                    fields_to_add = {
                        "name": [{"id":str(names[index])}],
                        "email": str(email),
                        "relevance": int(parsed["scores"]["relevance"]),
                        "depth": int(parsed["scores"]["depth"]),
                        "clarity": int(parsed["scores"]["clarity"]),
                        "originality": int(parsed["scores"]["originality"]),
                        "total_score": int(parsed["total_score"]),
                        "feedback": str(parsed["feedback"]),
                        "parent_record_id": [payload['record_id']],  # ✅ wrap in a list
                        "file": [{"file_token": payload["file"][0]['file_token']}],
                        "trainer":[{"id":payload["uploaded_by"]["id"]}]
                    }

                    self.ctx.base_manager.create_record(
                        table_id=os.getenv('PROCESSED_TABLE_ID'),
                        fields=fields_to_add
                    )

                    
                self.ctx.base_manager.update_record(
                        table_id=os.getenv('UNPROCESSED_TABLE_ID'),
                        record_id=payload['record_id'],
                        fields={
                            "status": 'done'
                        }
                    )
                self.ctx.logger.info("Done")

            else:
                self.ctx.logger.warning("⚠️ No data to process in Excel.")

        except Exception as e:
            self.ctx.logger.error(f"❌ Error during realization evaluation: {e}")

        self.ctx.logger.info("✅ Finished realization evaluation.")
        
