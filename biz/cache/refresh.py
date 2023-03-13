from client.log import logger
from biz.cache import session
from biz import routine_spliter
import time
import threading


def task():
    while True:
        logger.info("excuteTask start")
        try:
            # 执行任务
            session_list = session.session_mng.clear_timeout_session()
            for session_id in session_list:
                content = session.session_mng.get_session_content(session_id)
                if routine_spliter.routine_valuable(content.get_messages()):
                    summary = routine_spliter.get_summary(content.get_messages())
                    routine_spliter.store_index(content, summary)
                else:
                    logger.info("session abandon: session_id: %s, user_name: %s", content.session_id, content.user_name)
                session.session_mng.remove_session_data(session_id)
        except Exception as e:
            logger.error("executeTask error: %s", e)
        time.sleep(5)


t = threading.Thread(target=task)

