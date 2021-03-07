# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

    Decorators:

        privileges(roles)

"""
from functools import wraps
from werkzeug.exceptions import Unauthorized, Forbidden
from src.models.user import User, ROLES


def privileges(roles):
    """
    Ensures the logged in user has the required privileges.

        Parameters:
            roles (ROLES): example: ROLES.MOD | ROLES.ADMIN
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(username, *args, **kwargs):
            user = User.objects(username=username).only("roles").first()

            if not user:
                raise Unauthorized()

            user_roles = ROLES(user.roles)

            # Check if the user has the required permission(s)
            if not(user_roles & roles):
                raise Forbidden()

            return f(username, *args, **kwargs)
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
        pass
    return decorator
