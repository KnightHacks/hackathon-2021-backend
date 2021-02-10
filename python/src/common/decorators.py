# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

    Decorators:

        privileges(roles)

"""
from functools import wraps
from werkzeug.exceptions import Unauthorized, Forbidden

from src.models.user import User

def privileges(*roles):
    """Ensures the logged in user has the required privileges."""
    def decorator(f):
        @wraps(f)
        def decorated_function(username, *args, **kwargs):
            user = User.objects(username=username).only("permissions").first()

            if not user:
                raise Unauthorized()

            # Check if the user has the required permission(s)
            if not any(True for r in user.privileges if r in roles):
                raise Forbidden()

            return f(username, *args, **kwargs)
        return decorated_function
    return decorator
