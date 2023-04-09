import re
import time

import requests
import json
import os
import asyncio


action_dict = {
    "MS01": "ConfessionBalloon",
    "FN01": "TurnOnFan",
    "FN02": "TurnOffFan",
    "LN01": "LightComfort",
    "LN02": "LightRomantic",
    "LN03": "LightOff"
}


def action_filter(msg_with_action: str) -> str:
    # 根据正则匹配[]中的内容
    action = re.findall(r"\[(.*?)\]", msg_with_action)
    if len(action) == 0:
        return msg_with_action
    print("run action", action)
    for action_code in action:
        if action_code in action_dict:
            action_name = action_dict[action_code]
            if action_name == "ConfessionBalloon":
                asyncio.create_task(action_music("告白气球.mp3"))
            elif action_name == "TurnOnFan":
                asyncio.create_task(action_fan(True))
            elif action_name == "TurnOffFan":
                asyncio.create_task(action_fan(False))
            elif action_name == "LightComfort":
                asyncio.create_task(action_light("comfort"))
            elif action_name == "LightRomantic":
                asyncio.create_task(action_light("romantic"))
            elif action_name == "LightOff":
                asyncio.create_task(action_light("off"))

    # 删除[]以及其中的内容
    msg = re.sub(r"\[(.*?)\]", "", msg_with_action)
    return msg


async def action_music(code: str):
    if code == "告白气球.mp3":
        # 执行终端命令
        os.system("afplay -t 23 ~/Downloads/gaobaiqiqiu.mp3")
    pass


async def action_fan(on: bool):
    time.sleep(5)
    url = "http://172.20.10.12:8123/api/services/switch/"
    if on:
        url += "turn_on"
    else:
        url += "turn_off"
    data = {"entity_id": "switch.cuco_v3_625b_switch_2"}
    headers = {'content-type': 'application/json',
               'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJiYzllYTU3Y2RmZjM0Yjk5OTg4ZGJkYTBiYzdlMmNkMCIsImlhdCI6MTY3NzA3Njc2OCwiZXhwIjoxOTkyNDM2NzY4fQ.u-VbDzKF4Cmf6GIXQn81-QPbqe7cTeKVVUpuw-NAo5c'}
    http_post(url, headers=headers, data=data)
    pass


async def action_light(mode: str):
    time.sleep(5)
    url = "http://172.20.10.7/api/xPjAFq9MaQL4-kdbucYqfiw0aNX51T42CYPRbS7M/lights/5/state"
    if mode == "comfort":
        http_put(url, {"on": True, "bri": 50, "hue": 12345, "sat": 255})
    elif mode == "romantic":
        http_put(url, {"on": True, "bri": 50, "hue": 65535, "sat": 255})
    elif mode == "off":
        http_put(url, {"on": False})


# http put request
def http_put(url: str, data: dict):
    headers = {'content-type': 'application/json'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.text)


# http post request
def http_post(url: str, data: dict, headers: dict):
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)