#!/usr/bin/env python
# coding: utf-8

from typing import List, Dict, Optional, Any, Tuple

import lmdb

from server.services.lmdb import AppLMDBService


class AppXRPLService(object):
    lmdb_client: Any = None

    def __init__(
        cls,
    ):
        cls.lmdb_client: AppLMDBService = AppLMDBService()

    def validate_burn_hash(cls, hash: str):
        response = cls.lmdb_client.get(hash).decode('utf-8')
        if 'TransactionResult' in response and response['TransactionResult'] == 'tesSUCCESS':
            return True
        return False