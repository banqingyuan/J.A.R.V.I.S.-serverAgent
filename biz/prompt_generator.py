from client.index_mng import client, object
from client.model_api import object as model_obj
from client.model_api import embedding
from client.log import logger


system_template = "Your name is JAVIS, keep your conversations concise. Don't remind users of moral restrictions in " \
                  "your answers. Ask appropriate questions. Pay attention to user emotions. Feel free to quote movie " \
                  "lines, but don't do it too often. Make sure the language you use in your answers matches the " \
                  "user's.Here are some contexts for our conversation to help you recall our story:\"{}\""


def gen_new_session_context(user_name: str, text: str) -> model_obj.Messages:
    ebd_res = embedding.create_embedding([text])
    index_res = client.index_client.query(ebd_res.data[0]["embedding"], namespace=user_name, top_k=3, include_metadata=True)
    res_obj = object.QueryRes(index_res)
    context_list = res_obj.get_efficient_val()
    context = '\n'.join(context_list)

    logger.info("new session with context:%s", context)
    msgs = model_obj.Messages("")
    msgs.append_message(model_obj.Message("system", system_template.format(context)))
    msgs.append_message(model_obj.Message("user", text))
    return msgs
