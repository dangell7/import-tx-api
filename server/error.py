#!/usr/bin/env python
# coding: utf-8

import json

class ApiError(Exception):
    """ApiError."""

    def __init__(self, error, status_code=None, headers=None):
        """__init__."""
        super(ApiError, self).__init__(error)

        self.error = error
        self.status_code = status_code
        self.headers = headers
    
    def to_dict(self):
        """Return a dictionary representation of the error."""
        return {
            'error': self.error,
            'status_code': self.status_code,
            'headers': self.headers
        }
    
    def __str__(self):
        """String representation of the error."""
        return json.dumps(self.to_dict())

    def __unicode__(self):
        """__unicode__."""
        return self.error


class BadRequestError(ApiError):
    """BadRequestError."""

    pass


class NotAuthorizedError(ApiError):
    """NotAuthorizedError."""

    pass


class NotFoundError(ApiError):
    """NotFoundError."""

    pass


class InternalServerError(ApiError):
    """InternalServerError."""

    pass


def bad_request_handler(error):
    return {
        "detail": str(error),
        "status": 400,
        "title": "Bad Request",
    }, 400


def not_auth_handler(error):
    return {
        "detail": str(error),
        "status": 401,
        "title": "Not Authorized",
    }, 401


def not_found_handler(error):
    return {
        "detail": str(error),
        "status": 404,
        "title": "Not Found",
    }, 404


def internal_handler(error):
    return {
        "detail": str(error),
        "status": 500,
        "title": "Internal Error",
    }, 500


def handle_error_code(e, status_code):
    if status_code == 400:
        raise BadRequestError(e)
    elif status_code == 401:
        raise NotAuthorizedError(e)
    elif status_code == 404:
        raise NotFoundError(e)
    elif status_code == 500:
        raise InternalServerError(e)
    else:
        raise InternalServerError(e)
