'''
meta_data是每条index的标签数据
index的可存放内容需要通过metad_data进行分类
当前的设计有用户对话摘要和行为日志摘要
{
    "tag": ["summary"],
    "ts": 202203121345,
    "routine_id": [],
    "type": "communicate|log"
    "text": ""
}
'''
import time
from typing import List

MetaType_Communication = "communication"


class MetaData:

    # new_meta_data ts格式统一为
    def new_meta_data(self):
        meta_data = {
            "type": self.type,
            "ts": self.ts,
            "text": self.text
        }
        if len(self.tag) > 0:
            meta_data["tag"] = self.tag
        if self.session_id != "":
            meta_data["session_id"] = [self.session_id]

        return meta_data

    def new_idx_id(self):
        id = str(self.ts)
        id = id + '_' + self.type
        if self.session_id != "":
            id = id + self.session_id
        return id

    def __init__(self, type: str, tag: List[str], text: str, ts: int = int(time.strftime("%Y%m%d%H%M", time.localtime())),
                 session_id: str = ""):
        self.type = type
        self.ts = ts
        self.tag = tag
        self.session_id = session_id
        self.text = text
