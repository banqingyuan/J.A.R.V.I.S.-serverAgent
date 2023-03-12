from typing import List
import json
import pickle


class Message:
    def get_content(self):
        return self.content

    def __init__(self, role, content):
        self.role = role
        self.content = content


class Messages:

    def gen_messages_req(self):
        messages = []
        for item in self.messages:
            msg = {}
            msg["role"] = item.role
            msg["content"] = item.content
            messages.append(msg)

        return messages

    def marshal_messages(self) -> str:
        tmp_lst = []
        for item in self.messages:
            tmp_dic = {}
            tmp_dic["role"] = item.role
            tmp_dic["content"] = item.content
            tmp_lst.append(tmp_dic)
        return json.dumps(tmp_lst)

    def append_message(self, msg: Message):
        self.messages.append(msg)
        return

    def get_messages(self):
        return self.messages

    def __init__(self, chat_content: str == ""):
        if chat_content == "":
            self.messages = []
        else:
            msgs_lst = []
            msgs_list_str = json.loads(chat_content)
            for v in msgs_list_str:
                if "role" not in v:
                    continue
                if "content" not in v:
                    continue
                msg = Message(v["role"], v["content"])
                msgs_lst.append(msg)
            self.messages = msgs_lst


class ChatResponse:
    def __init__(self, data):
        self.id = data['id']
        self.object = data['object']
        self.created = data['created']
        self.model = data['model']
        self.usage = data['usage']
        self.choices = data['choices']

    def get_message(self) -> Message:
        return Message(self.choices[0]['message']['role'], self.choices[0]['message']['content'])

    def get_finish_reason(self):
        return self.choices[0]['finish_reason']

    def get_prompt_tokens(self):
        return self.usage['prompt_tokens']

    def get_completion_tokens(self):
        return self.usage['completion_tokens']

    def get_total_tokens(self):
        return self.usage['total_tokens']

    def to_str(self):
        data = {
            'id': self.id,
            'object': self.object,
            'created': self.created,
            'model': self.model,
            'usage': self.usage,
            'choices': self.choices
        }
        return json.dumps(data)

