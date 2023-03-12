import json

from client.model_api import object, query, embedding
from client.index_mng import client,meta
from biz.cache import object as session_object
from client.log import logger


# 判断一个session对话信息的保存价值，当前没有很行之有效的办法
# 思路1：判断对话的轮数
# 思路2：判断token的长度
# 思路3：判断该summary与已有summary的相关度
# 思路4：让chatGPT辅助判断，只要调试prompt即可
def routine_valuable(messages: object.Messages) -> bool:
    msgs = object.Messages("")
    for msg in messages.get_messages():
        if msg.role == "system":
            continue
        msgs.append_message(msg)

    if len(msgs.get_messages()) > 6:
        return True
    return False


prompt_to_summary = 'The following are some conversation data, please help me summarize the conversation summary in ' \
                    'English, please don’t miss the key details, don’t need to be too general, just simplify.'


def get_summary(messages: object.Messages) -> str:
    msg_str = messages.marshal_messages()
    prompt = prompt_to_summary + '\n' + msg_str
    return query.completion(prompt)


def store_index(session_data: session_object.SessionData, summary):
    ebd_res = embedding.create_embedding([summary])
    meta_data = meta.MetaData(meta.MetaType_Communication, [], session_id=session_data.session_id, text=summary)
    id = meta_data.new_idx_id()
    data = meta_data.new_meta_data()
    client.index_client.upsert([id, ebd_res.data[0]["embedding"], data], namespace=session_data.user_name)
    logger.info("store index success: user_name: %s, idx_id: %s, meta_data:%s", session_data.user_name, id, json.dumps(meta_data))
