from client.log import logger

class IndexRes:
    def __init__(self, text, metadata):
        self.text = text
        self.score = metadata


class QueryRes:
    def __init__(self, dict_data):
        self.matches = dict_data['matches']
        self.namespace = dict_data['namespace']

    # 三段有价值的对话摘要
    def get_efficient_val(self):
        context_list = []
        for item in self.matches:
            if item["score"] > 0.7:
                context_list.append(item["metadata"]["text"])
            else:
                logger.info("drop context: score: %f", item["score"])
        return context_list
