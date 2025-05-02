import os
import lark_oapi as lark
from lark_oapi.api.auth.v3 import *
from lark_oapi.core.const import UTF_8
from .Lark import Lark
import json

class TenantManager:
    def __init__(self, lark_client: Lark):
        self.lark = lark_client.client
        self.APP_ID = os.getenv('APP_ID')
        self.APP_SECRET = os.getenv('APP_SECRET')

    def get_tenant_access_token(self):
        request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
            .request_body(InternalTenantAccessTokenRequestBody.builder() \
                          .app_id(self.APP_ID)
                          .app_secret(self.APP_SECRET)
                          .build()) \
            .build()

        response: InternalTenantAccessTokenResponse = self.lark.auth.v3.tenant_access_token.internal(request)
        if not response.success():
            lark.logger.error(
                f"client.auth.v3.tenant_access_token.internal failed, code: {response.code}, msg: {response.msg} log_id: {response.get_log_id()}"
            )

            return
        data = json.loads(response.raw.content.decode('UTF-8'))
        # tenant_access_token = data["tenant_access_token"]
        # print('data', data["tenant_access_token"])
        # lark.logger.info(f"Get Tenant Token: {tenant_access_token}")

        return data["tenant_access_token"]