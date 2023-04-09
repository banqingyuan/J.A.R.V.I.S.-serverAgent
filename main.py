import fastapi
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
import uvicorn
import logging

import handler.voice_handler as vh
# 导入Request上下文对象，用来在前后台之间传递参数
from starlette.requests import Request
import os
import Init

app = FastAPI()


class request(BaseModel):
    user_name: str       # 姓名
    msg: str        # 年龄

@app.post("/voice/text/report")
async def voice_text_handler(req: request):
    return vh.voice_handler(req.user_name, req.msg)


Init.MustInit()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
