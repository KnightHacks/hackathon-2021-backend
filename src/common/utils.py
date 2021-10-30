# -*- coding: utf-8 -*-
"""
    src.common.utils
    ~~~~~~~~~~~~~~~~

"""
from flask import _request_ctx_stack, has_request_context, request
from werkzeug.local import LocalProxy
from werkzeug.exceptions import Unauthorized

current_user = LocalProxy(lambda: _get_user())


def _get_user():
    if (has_request_context()
            and not hasattr(_request_ctx_stack.top, "current_user")):
        pass  # TODO: load user

    return _request_ctx_stack.top.current_user


def _get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Unauthorized("Authorization header is expected")

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise Unauthorized("Authorization header must start with Bearer")

    elif len(parts) == 1:
        raise Unauthorized("Token not found")

    elif len(parts) > 2:
        raise Unauthorized("Authorization header must be a Bearer token")

    token = parts[1]
    return token
