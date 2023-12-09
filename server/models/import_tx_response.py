# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from server.models.base_model_ import Model
from server import util


class ImportTxResponse(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, tx: Dict[str, object]=None, meta: Dict[str, object]=None):  # noqa: E501
        """ImportTxResponse - a model defined in Swagger

        :param tx: The tx of this ImportTxResponse.  # noqa: E501
        :type tx: Dict[str, object]
        :param meta: The meta of this ImportTxResponse.  # noqa: E501
        :type meta: Dict[str, object]
        """
        self.swagger_types = {
            'tx': Dict[str, object],
            'meta': Dict[str, object]
        }

        self.attribute_map = {
            'tx': 'tx',
            'meta': 'meta'
        }
        self._tx = tx
        self._meta = meta

    @classmethod
    def from_dict(cls, dikt) -> 'ImportTxResponse':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ImportTxResponse of this ImportTxResponse.  # noqa: E501
        :rtype: ImportTxResponse
        """
        return util.deserialize_model(dikt, cls)

    @property
    def tx(self) -> Dict[str, object]:
        """Gets the tx of this ImportTxResponse.


        :return: The tx of this ImportTxResponse.
        :rtype: Dict[str, object]
        """
        return self._tx

    @tx.setter
    def tx(self, tx: Dict[str, object]):
        """Sets the tx of this ImportTxResponse.


        :param tx: The tx of this ImportTxResponse.
        :type tx: Dict[str, object]
        """
        if tx is None:
            raise ValueError("Invalid value for `tx`, must not be `None`")  # noqa: E501

        self._tx = tx

    @property
    def meta(self) -> Dict[str, object]:
        """Gets the meta of this ImportTxResponse.


        :return: The meta of this ImportTxResponse.
        :rtype: Dict[str, object]
        """
        return self._meta

    @meta.setter
    def meta(self, meta: Dict[str, object]):
        """Sets the meta of this ImportTxResponse.


        :param meta: The meta of this ImportTxResponse.
        :type meta: Dict[str, object]
        """
        if meta is None:
            raise ValueError("Invalid value for `meta`, must not be `None`")  # noqa: E501

        self._meta = meta