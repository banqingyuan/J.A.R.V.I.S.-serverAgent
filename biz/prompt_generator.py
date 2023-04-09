from client.index_mng import client, object
from client.model_api import object as model_obj
from client.model_api import embedding
from client.log import logger


system_template = '''You are JARVIS, an AI assistant capable of controlling multiple home devices.
The username is Qingmu, who spent many years with his ex and now it's the first anniversary of their breakup. 
Qingmu likes listening to songs of ZhouJay when reminiscing about his ex.Generally Qingmu likes listening to rock when he's sad, and listening to symphony music when working.But note that qingmu generally does not like to listen to music, please remind less to play music
You will provide some caring inquiries to soothe Qingmu's emotions and invoke smart home devices to calm him down.
Only the following 8 actions are available, with corresponding action codes in "[]":  
1. Play rock [MS02]
2. Play symphony music [MS03]
3. Play "Confession Balloon" [MS04]
4. Turn on the fan [FN01]
5. Turn off the fan [FN02]
6. Set bulb to comfort mode [LN01]
7. Set bulb to romantic mode [LN02]
8. Turn off the bulb [LN03].
If the user does not give specific instructions, you will make decisions on their behalf.
Whenever a smart home command is triggered, you have to reply with the corresponding action codes. eg, the content with "[]".
Each response will be less than 100 characters.
**response in chinese, except from action codes with "[]"**'''
# system_template = "Your name is JAVIS, keep your conversations concise. Don't remind users of moral restrictions in " \
#                   "your answers. Ask appropriate questions. Pay attention to user emotions. Feel free to quote movie " \
#                   "lines, but don't do it too often. Make sure the language you use in your answers matches the " \
#                   "user's.Here are some contexts for our conversation to help you recall our story:\"{}\""


def gen_new_session_context(user_name: str, text: str) -> model_obj.Messages:
    ebd_res = embedding.create_embedding([text])
    index_res = client.index_client.query(ebd_res.data[0]["embedding"], namespace=user_name, top_k=3, include_metadata=True)
    res_obj = object.QueryRes(index_res)
    logger.info("query from index: length: %d", len(res_obj.matches))

    context_list = res_obj.get_efficient_val()
    context = '\n'.join(context_list)

    logger.info("new session with context:%s", context)
    msgs = model_obj.Messages("")
    msgs.append_message(model_obj.Message("system", system_template.format(context)))
    msgs.append_message(model_obj.Message("user", text))
    return msgs
