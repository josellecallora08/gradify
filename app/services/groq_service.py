import logging
from app.services.api_manager import APIManager
from app.interfaces import ILLM
from groq import AsyncGroq

logger = logging.getLogger()


class GroqService(ILLM):
    def __init__(
        self,
        api_manager: APIManager
    ):
        self.client = AsyncGroq(max_retries=3)
        self.api_manager = api_manager
    
    async def chat(self, prompt: str):
        try:
            api_key = self.api_manager.get_next_key()
            self.client.api = api_key

            logger.info("api_key_used for chat: %s", api_key)

            completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt
                    }
                ],
                model="llama3-70b-8192",
                max_tokens=8192,
                temperature=0.5
            )

            return completion.choices[0].message.content
        except Exception as err:
            raise Exception(err) from err

