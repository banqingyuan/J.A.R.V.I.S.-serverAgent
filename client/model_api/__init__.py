import openai
import os

key = os.environ.get("openai_app_key", "")
if key == "":
    raise Exception('openai_app_key not config')
else:
    openai.api_key = key
