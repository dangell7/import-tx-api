#!/usr/bin/env python
# coding: utf-8

from typing import List, Dict, Optional, Any, Tuple

import lmdb


class AppLMDBService(object):
    client: Any = None

    def __init__(cls):
        cls.client = lmdb.open('mylmdb', max_dbs=1)

    def create(cls, key: str, data: bytes):
        with cls.client.begin(write=True) as txn:
            txn.put(key.encode('utf-8'), data)
    
    def get(cls, key: str):
        with cls.client.begin(write=True) as txn:
            return txn.get(key.encode('utf-8'))