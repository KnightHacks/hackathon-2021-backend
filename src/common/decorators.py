# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

    Decorators:

        privileges(roles)

"""
from flask import request, current_app
from functools import wraps
from werkzeug.exceptions import Forbidden, Unauthorized
from src.models.user import User, ROLES
from src.models.tokenblacklist import TokenBlacklist
from src.common.jwt import decode_jwt


def privileges(roles):
    """
    Ensures the logged in user has the required privileges.

        Parameters:
            roles (ROLES): example: ROLES.MOD | ROLES.ADMIN
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(user, *args, **kwargs):
            user_roles = ROLES(user.roles)

            """ Check if the user has the required permission(s) """
            if not(user_roles & roles):
                raise Forbidden()

            return f(user, *args, **kwargs)
        return decorated_function
    return decorator


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

        user = User.objects(username=decoded_token["sub"]).first()

        if not user:
            raise Forbidden()

        if user.username != fromBL.user.username:
            raise Forbidden()

        return f(user, *args, **kwargs)

    return decorator
