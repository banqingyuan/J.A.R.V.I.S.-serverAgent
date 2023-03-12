import json

from biz.cache import object as cache_object
from client.model_api import object as model_object
from client.model_api import query
from client.log import logger


def talking_to_chatbot(session_data: cache_object.SessionData, text: str):
    # nick_name 暂时默认user
    session_data.chat_content_single_append(model_object.Message("user", text))

    chat_req = session_data.get_messages().gen_messages_req()
    resp = query.chat(chat_req)
    session_data.chat_content_single_append(resp.get_message())

    logger.info("session_id: %s,\n request: %s, \n resp: %s", session_data.session_id, json.dumps(chat_req), resp.to_str())
    return resp.get_message().get_content()
