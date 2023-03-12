from client.model_api import query
from client.model_api import embedding
from client.index_mng import client
from client.unitTest import const
from consdef import const as const2
from client.index_mng import meta
import unittest
from unittest import TestCase


class TestEmbedding(TestCase):
    text_list = [
        "我有一个hackathon的项目是希望做一个人工智能助手，可以帮你处理生活日常事务，控制你智能家居，和你进行有上下文理解能力的聊天",
        "我还有一个MR虚拟现实项目，让用户体验MR交互的魅力，在线下和你的朋友一起打地鼠，不过游戏画面是虚拟的，它通过MR眼镜显示在你面前的桌面上"
    ]

    def test_embedding(self):
        res = embedding.create_embedding(self.text_list)
        self.assertEqual(len(res.data), len(self.text_list))

        return res

    def test_upsert_index(self):
        res = self.test_embedding()
        meta_gen0 = meta.MetaData(meta.MetaType_Communication, [], self.text_list[0])
        meta_gen1 = meta.MetaData(meta.MetaType_Communication, [], self.text_list[1])

        meta_data0 = meta_gen0.new_meta_data()
        meta_data1 = meta_gen1.new_meta_data()

        idx_id0 = meta_gen0.new_idx_id() + "0"
        idx_id1 = meta_gen1.new_idx_id() + "1"

        self.assertIsNotNone(meta_data0)
        self.assertIsNotNone(meta_data1)

        self.idx.upsert([(idx_id0, res.data[0]["embedding"], meta_data0), (idx_id1, res.data[1]["embedding"], meta_data1)])

        query_source = "你还记得我跟你聊过的智能助手的项目吗？"
        response = embedding.create_embedding([query_source])
        query_res = self.idx.query(vector=response.data[0]["embedding"],top_k=2, include_metadata=True)
        print(query_res)
        self.assertEqual(len(query_res['matches']), 2)

        self.idx.delete([idx_id0,idx_id1,"202303121514_communication"])
        vec = self.idx.fetch([idx_id0,idx_id1])
        self.assertEqual(len(vec['vectors']), 0)

    def setUp(self):
        self.idx_name = const.idx_name
        self.idx = client.index_get(self.idx_name)


if __name__ == '__main__':
    unittest.main()
