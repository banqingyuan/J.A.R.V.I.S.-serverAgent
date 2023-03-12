from client.model_api import query
from client.model_api import embedding
from client.model_api import object
from unittest import TestCase
import unittest


# def test_query():
#     query_content = "who was the 12th person on the moon and when did they land?"
#     print(query.completion(query_content))
#
# def test_embedding():
#     text_list = [
#         "Sample document text goes here",
#         "there will be several phrases in each batch"
#     ]
#     res = embedding.create_embedding(text_list)
#     print(len(res.data[0]['embedding']))

class TestEmbedding(TestCase):
    msg_str = "[{\"role\": \"system\", \"content\": \"The background information is that last week the user mentioned to you the girl he met in the company who had brown hair and black eyes and spoke very interestingly. They talked about the latest natural language model ChatGPT and his planned downstream application \\\"Jaevis\\\", and the user felt very in tune with this girl.\"}, {\"role\": \"user\", \"content\": \"Do you remember the girl I told you last week\"}]"
    def test_message(self):
        msgs = object.Messages(self.msg_str)
        strs = msgs.marshal_messages()
        self.assertEqual(self.msg_str, strs)
        req = msgs.gen_messages_req()

        self.assertIsNotNone(len(req), 2)


    def setUp(self):
        return



if __name__ == '__main__':
    unittest.main()
