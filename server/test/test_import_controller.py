#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import

from flask import json

from server.models.import_tx_request import ImportTxRequest  # noqa: E501
from server.test import BaseTestCase


class TestIPNSontroller(BaseTestCase):
    """TestImportontroller integration test stubs"""

    def test_import_publish(cls):
        """Test case for import_tx

        Resend verification email
        """
        query_string = [('tx_hash', 'DEADBEEF')] 
        response = cls.client.open(
            '/v1/import/tx',
            method='GET',
            content_type='application/json',
            query_string=query_string
        )
        cls.assert200(
            response,
            'Response body is : ' + response.data.decode('utf-8')
        )

if __name__ == '__main__':
    import unittest
    unittest.main()
