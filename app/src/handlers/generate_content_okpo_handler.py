import pandas as pd
import os
import re
import json
from dotenv import load_dotenv
from app.interfaces import CallbackHandler
from app.common import AppContext
import requests
from typing import Dict
from youtube_transcript_api import YouTubeTranscriptApi
from app.services import OkpoProcessEndpoint
import time

load_dotenv('.env', override=True)


class ContentGenerator(CallbackHandler):
    def __init__(self, context: AppContext):
        self.ctx = context
        self.assistant_id: str = os.getenv('ASSISTANT_ID')
        self.api_token: str = os.getenv("OKPO_API_TOKEN")
        self.create_thread_and_run_endpoint = "https://okpo.com/version-test/api/1.1/wf/create_thread_and_run"
        self.add_run_message_endpoint = "https://okpo.com/version-test/api/1.1/wf/add_run_message"
        self.retrieve_run_endpoint = "https://okpo.com/version-test/api/1.1/wf/retrieve_run"
        self.retrieve_run_message_endpoint = "https://okpo.com/version-test/api/1.1/wf/retrieve_run_message"
        self.get_assistant_endpoint = "https://okpo.com/version-test/api/1.1/wf/get_assistant"

    def extract_video_id(self, url: str) -> str:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
        if not match:
            raise ValueError("Invalid Youtube URL")
        return match.group(1)

    def get_transcript(self, video_id: str) -> str:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry['text'] for entry in transcript])

    async def handler(self, payload: Dict[str, str]):
        self.ctx.logger.info("📝 Starting realization evaluation...")
        try:
            print(payload['record_id'])
            youtube_url = payload['youtube_link']['text']
            print(youtube_url)

            video_id = self.extract_video_id(youtube_url)
            transcript = self.get_transcript(video_id)


            # transcript_parts = []
            num_parts = 5
            # part_length = len(transcript) // num_parts if len(transcript) > num_parts else len(transcript)
            # for i in range(num_parts):
            #     start = i * part_length
            #     # For the last part, take the rest of the transcript
            #     end = (i + 1) * part_length if i < num_parts - 1 else len(transcript)
            #     part = transcript[start:end].strip()
            #     if part:
            #         transcript_parts.append(part)

            # Array to save each message/response from the conversation
            conversation_parts = []

            thread_id = None  # In a real app, this could come from a database, session, or client request

            for idx in range(num_parts):
                if thread_id:
                    # If thread exists, add a run message to the existing thread
                    add_run_response = OkpoProcessEndpoint.add_run_message(self, message=f"send me part {idx + 1}", thread_id=thread_id)
                    print(f"add_run_message response for part {idx+1}:", add_run_response)
                    run_id = add_run_response['response'].get('run_id')
                    if not run_id:
                        raise Exception("Failed to retrieve run_id after adding run message.")
                else:
                    # If thread does not exist, create a new thread and run, and save the thread_id
                    response = OkpoProcessEndpoint.create_thread_and_run(self, message=f"Create the first part of the story")
                    print(f"create_thread_and_run response for part {idx+1}:", response)
                    thread_id = response['response'].get('thread_id')
                    run_id = response['response'].get('run_id')
                    if not thread_id or not run_id:
                        raise Exception("Failed to create thread and run.")

                # Poll for run completion before retrieving the run message
                max_retries = 30
                delay_seconds = 2
                for attempt in range(max_retries):
                    run_status_response = OkpoProcessEndpoint.retrieve_run(self, thread_id=thread_id, run_id=run_id)
                    print(f"retrieve_run response for part {idx+1}:", run_status_response)
                    status = run_status_response['response'].get('status')
                    if status == "completed":
                        break
                    elif status in ("failed", "cancelled"):
                        raise Exception(f"Run ended with status: {status}")
                    time.sleep(delay_seconds)
                else:
                    raise Exception("Run did not complete in expected time.")

                # Now retrieve the run message for this part and save it
                message = OkpoProcessEndpoint.retrieve_run_message(self, thread_id=thread_id, run_id=run_id)
                print(f"Retrieved message for part {idx+1}:", message)
                conversation_parts.append({
                    "part": idx + 1,
                    "response": message['response']['message']
                })

                markdown_prompt = """
- You are a helpful and focused AI assistant tasked to respond strictly based on the structured transcript provided below. Your role is not to create, assume, or invent new context — onlywork with what is written under each `### Part`.

- Do not answer until all parts are reviewed or the user directs you to a specific part.
              
- Summarize, reframe, or continue the discussion based on the structured inputs from a video transcript broken into several meaningful parts. Keep tone friendly, but informative.

- 🤖 AI BEHAVIOR
- Wait for user input before generating any follow-up.
- Focus only on content within the transcript parts.
- Do not reference external data or historical facts.
- Speak conversationally, but remain on-topic.
- Follow the logical flow from Part 1 to Part 5 when asked to continue.

- 🚫 GUARDRAILS
- ❌ Do not add your own opinions.
- ❌ Do not mention knowledge outside the provided transcript.
- ❌ Do not interpret user intent unless explicitly asked.
- ❌ Do not summarize or skip parts unless directed.

- 🛠️ FORMAT
The transcript is broken into labeled parts:
- Use `## Part N` to identify sections.
- Each part is independent but follows a logical story arc.
- Assume all content was said by the same person.
- 📚 CONVERSATION TRANSCRIPT
                """
                # Add each part of the transcript
                for part in conversation_parts:
                    markdown_prompt += f"\n\n## Part {part['part']}\n\n{part['response'].strip()}"

                prompt = markdown_prompt.strip()

                fields_to_add = {
                    "link": payload['youtube_link'],
                    "parent_record_id": [payload['record_id']],
                    "prompt": prompt,
                    "transcript": transcript,
                    "requestor": [{"id": payload["uploaded_by"][0]["id"]}]
                }

            self.ctx.base_manager.create_record(
                table_id=os.getenv('PROCESSED_TABLE_ID'),
                fields=fields_to_add
            )

            self.ctx.base_manager.update_record(
                table_id=os.getenv('UNPROCESSED_TABLE_ID'),
                record_id=payload['record_id'],
                fields={"status": 'done'}
            )


        except Exception as e:
            self.ctx.logger.error(f"❌ Error during realization evaluation: {e}")
            self.ctx.base_manager.update_record(
                table_id=os.getenv('UNPROCESSED_TABLE_ID'),
                record_id=payload['record_id'],
                fields={"status": 'invalid_url'}
            )

        finally:
            self.ctx.logger.info("✅ Finished realization evaluation.")
