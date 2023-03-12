from biz.cache import session
from biz import chat_bot


def voice_handler(user_name,text):
    session_id = session.session_mng.get_vaild_session_id(user_name, text)
    data = session.session_mng.get_session_content(session_id)

    return chat_bot.talking_to_chatbot(data, text)
