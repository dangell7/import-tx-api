#!/usr/bin/env python
# coding: utf-8

import logging
import connexion
from typing import Dict, Any

# server
from server.models.import_tx_response import ImportTxResponse  # noqa: E501
from server.error import (
    BadRequestError,
    NotAuthorizedError,
    NotFoundError,
    InternalServerError,
    bad_request_handler,
    not_auth_handler,
    not_found_handler,
    internal_handler,
)
from server.services.lmdb import AppLMDBService
# 
# Create Logger
logger = logging.getLogger("app")


def import_tx(hash_id: str = None):  # noqa: E501
    """Lookup an import tx by hash

     # noqa: E501

    :param body: Hash to lookup
    :type body: dict | bytes

    :rtype: ImportTxRequest
    """
    try:
        client = AppLMDBService()
        response = client.get(hash_id)
        if response:
            return ImportTxResponse(response.decode('utf-8'))
        
        return ImportTxResponse(response)

    except BadRequestError as e:
        # Handle bad request error
        logger.error(f'BadRequestError: {str(e)}')
        return bad_request_handler(e)
    except NotAuthorizedError as e:
        # Handle not authorized error
        logger.error(f'NotAuthorizedError: {str(e)}')
        return not_auth_handler(e)
    except NotFoundError as e:
        # Handle not found error
        logger.error(f'NotFoundError: {str(e)}')
        return not_found_handler(e)
    except InternalServerError as e:
        # Handle internal server error
        logger.error(f'InternalServerError: {str(e)}')
        return internal_handler(e)
    except Exception as e:
        # Handle other exceptions
        logger.error(f'Exception: {str(e)}')
        return internal_handler(e)
    

