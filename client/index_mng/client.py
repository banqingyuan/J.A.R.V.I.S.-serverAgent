from config.conf import config_mng
from client import index_mng


def index_get(idx_name):
    return index_mng.pinecone.Index(idx_name)


def index_create(idx_name, dim=1536, timeout=10):
    index_mng.pinecone.create_index(idx_name, dimension=dim, timeout=timeout)


def index_delete(idx_name, timeout=10):
    return index_mng.pinecone.delete_index(idx_name, timeout)


def index_describe(idx_name, timeout=10):
    return index_mng.pinecone.describe_index(idx_name)


def index_exist(idx_name, timeout=10):
    try:
        describe = index_describe(idx_name)
        if describe.status is not None:
            if describe.status['ready']:
                return True
        return False
    except:
        return False


index_client = index_mng.pinecone.Index(index_name=config_mng.get_index_name())


