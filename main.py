import fastapi
from fastapi import FastAPI
import logging

from starlette.responses import FileResponse
import handler.voice_handler as vh
# 导入Request上下文对象，用来在前后台之间传递参数
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import os
import Init

app = FastAPI()

logger = logging.getLogger("fastapi")
logger.setLevel(logging.INFO)

templates = Jinja2Templates(directory='templates')


@app.get("/voice/text/report")
async def voice_text_handler(user_name: str, text: str):
    return vh.voice_handler(user_name, text)


Init.MustInit()
