from .Lark import Lark
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageResponse, CreateMessageRequestBody

class LarkMessenger:
    def __init__(self, lark: Lark) -> None:
        self.client = lark.client
    
    async def send_message_card_to_group_chat(self, group_chat_id: str, content: str):
        create_message_request: CreateMessageRequest = CreateMessageRequest.builder() \
            .receive_id_type('chat_id') \
            .request_body(
                CreateMessageRequestBody.builder() \
                    .receive_id(group_chat_id) \
                    .msg_type("interactive") \
                    .content(content) \
                    .build()
            ) \
            .build()
        
        response: CreateMessageResponse = await self.client.im.v1.message.acreate(create_message_request)

        if response.code != 0:
            raise Exception(f"Error: code={response.code}, message={response.msg}")

        return response