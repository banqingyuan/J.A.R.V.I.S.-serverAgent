from client import model_api
from client.index_mng import client
from config import conf
from biz.cache import refresh


def MustInit():
    index_name = conf.config_mng.get_index_name()
    if client.index_exist(index_name) is not True:
        client.index_create(index_name, timeout=20 * 60)
    refresh.t.start()
