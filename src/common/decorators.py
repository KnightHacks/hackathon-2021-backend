# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

    Decorators:

        privileges(roles)

"""
from flask import request, current_app 
from flask_security import current_user
from functools import wraps
from werkzeug.exceptions import Forbidden, Unauthorized
from src.models.user import User
from src.models.tokenblacklist import TokenBlacklist
from src.common.jwt import decode_jwt

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
        elif current_app.config.get("TESTING"):
            token = request.headers.get("sid")

        if not token:
            raise Unauthorized("User is not signed in!")

        decoded_token = decode_jwt(token)

        fromBL = TokenBlacklist.findOne(
            jti=decoded_token["jti"],
            revoked=False
        )

        if not fromBL:
            raise Unauthorized("User is not signed in!")

        user = current_app.hacker_datastore.find_user(username=decoded_token["sub"])
        current_user = user
        if current_user.has_role('hacker'):
            print('Has Hacker Role')
        else:
            print('nope')

        if not user:
            raise Forbidden()

        if user.username != fromBL.user.username:
            raise Forbidden()

        return f(user, *args, **kwargs)

    return decorator
