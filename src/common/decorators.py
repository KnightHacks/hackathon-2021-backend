# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

"""
from flask import request, current_app as app
from functools import wraps
from werkzeug.exceptions import Unauthorized, NotFound
from src.models.user import User


def authenticate(f):
    """
    Authenticated the user using a header.
    """

    doc = getattr(f, "__doc__")
    if doc:
        setattr(f, "__doc__", doc + """security:
        - CookieAuth: []""")

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if request.cookies.get("sid"):
            token = request.cookies.get("sid")
        elif app.config.get("TESTING"):
            token = request.headers.get("sid")

        if not token:
            raise Unauthorized("User is not signed in!")

        data = User.decode_auth_token(token)
        user = User.objects(username=data).first()

        if not user:
            raise NotFound()

        return f(user, *args, **kwargs)

    return decorator
