from hashlib import md5
import time
from typing import List
from biz.cache import object
from biz import prompt_generator as generator
from client import log


class InVaildSessionException(Exception):
    pass


# 当前是单实例部署，缓存放在本地，多实例应该放在redis来保证一致性，或者使用一致性哈希
def gen_session_id(user_name, timestamp) -> str:
    source = str(user_name) + str(timestamp)
    session_id = md5(source.encode('utf8')).hexdigest()
    return session_id


class SessionMng:

    def __refresh_session_life(self, session_id):
        self.session_ts[session_id] = time.time() * 1000

    def get_session_content(self, session_id) -> object.SessionData:
        if session_id not in self.session_cache:
            log.logger.error("session_id not found in session_cache, id:%s", session_id)
            raise InVaildSessionException
        else:
            self.__refresh_session_life(session_id)
            return self.session_cache[session_id]

    def delete_session(self, session_id):
        self.session_cache.pop(session_id)

    def get_vaild_session_id(self, user_name, text:str):
        if user_name in self.user_to_session:
            session_id = self.user_to_session[user_name]
            self.__refresh_session_life(session_id=session_id)
            return session_id

        # 生成新的会话上下文
        msgs = generator.gen_new_session_context(user_name, text)

        # 生成sessionId
        session_id = gen_session_id(user_name, timestamp=time.strftime('%Y%m%d%H%M%S', time.localtime()))

        # 组装session数据
        session_data = object.SessionData(session_id, msgs, user_name)

        # 更新session_mng
        self.session_cache[session_id] = session_data
        self.__refresh_session_life(session_id)
        self.user_to_session[user_name] = session_id
        return session_id

    def update_session(self, session_data: object.SessionData):
        self.__refresh_session_life(session_id=session_data.session_id)
        self.session_cache[session_data.session_id] = session_data

    def remove_session_data(self, session_id):
        self.session_cache.pop(session_id)
        self.session_ts.pop(session_id)

    def clear_timeout_session(self):
        session_list = []
        now_ts = time.time() * 1000
        life_time = 1 * 60 * 1000  # session的不活跃生存时间为十分钟
        for session_id, ts in self.session_ts.items():
            if now_ts - ts > life_time:
                # 先删除user索引，用户就不会再使用这段session，具体的session数据需要数据处理后异步删除
                session_data = self.session_cache[session_id]
                self.user_to_session.pop(session_data.user_name)
                session_list.append(session_id)
        return session_list

    '''
    session_cache
    {
        "$session_id": {
            "chat_content": [
            {"role": "system", "content": "The background information is that last week the user mentioned to you the girl he met in the company who had brown hair and black eyes and spoke very interestingly. They talked about the latest natural language model ChatGPT and his planned downstream application \"Jaevis\", and the user felt very in tune with this girl."},
            {"role": "user", "content": "Do you remember the girl I told you last week"}
            ]
        }
    }
    '''
    def __init__(self):
        self.session_cache = {}
        self.user_to_session = {}
        self.session_ts = {}
        return


session_mng = SessionMng()
