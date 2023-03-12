from client.model_api import object
from typing import List


class SessionData:

    def marshal(self):
        return

    def chat_content_single_append(self, msg: object.Message):
        self.messages.append_message(msg)
        return

    def get_messages(self) -> object.Messages:
        return self.messages

    def __init__(self, session_id: str, msgs: object.Messages, user_name: str):
        self.session_id = session_id
        self.messages = msgs
        self.user_name = user_name


