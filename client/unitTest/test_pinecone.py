from client.index_mng import client
from unittest import TestCase
from client.unitTest import const

def test_create_index():
    client.index_create(const.idx_name)


def test_delete_index():
    client.index_delete(const.idx_name)


def test_index_exist():
    print(client.index_exist(const.idx_name))


if __name__ == '__main__':
    test_create_index()
    #test_delete_index()
    test_index_exist()
