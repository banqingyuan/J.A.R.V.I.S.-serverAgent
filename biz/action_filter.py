import re
import requests
import json

action_dict = {
    "MS04": "ConfessionBalloon",
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
                action_music("告白气球.mp3")
            elif action_name == "TurnOnFan":
                action_fan(True)
            elif action_name == "TurnOffFan":
                action_fan(False)
            elif action_name == "LightComfort":
                action_light("comfort")
            elif action_name == "LightRomantic":
                action_light("romantic")
            elif action_name == "LightOff":
                action_light("off")

    # 删除[]以及其中的内容
    msg = re.sub(r"\[(.*?)\]", "", msg_with_action)
    return msg


def action_music(code: str):
    print("action_music", code)
    pass


def action_fan(on: bool):
    print("action_fan", on)
    pass


def action_light(mode: str):
    url = "http://172.20.10.7/api/xPjAFq9MaQL4-kdbucYqfiw0aNX51T42CYPRbS7M/lights/5/state"
    if mode == "comfort":
        http_put(url, {"on": True, "bri": 255, "hue": 12345, "sat": 255})
    elif mode == "romantic":
        http_put(url, {"on": True, "bri": 255, "hue": 65535, "sat": 255})
    elif mode == "off":
        http_put(url, {"on": False})


# http put request
def http_put(url: str, data: dict):
    headers = {'content-type': 'application/json'}
    r = requests.put(url, data=json.dumps(data), headers=headers)
    print(r.text)
