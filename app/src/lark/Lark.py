import lark_oapi as lark
import os


class Lark(lark.Client):
    def __init__(self, app_id=None, app_secret=None, debug=False):
     
        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \

        if debug:
            self.client = self.client.log_level(lark.LogLevel.DEBUG)

        self.client = self.client.build()