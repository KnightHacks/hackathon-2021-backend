from functools import wraps
from werkzeug.exceptions import Unauthorized, Forbidden

from src.models.hacker import Hacker, HackerRole

def privileges(roles):
    """Ensures the logged in hacker has the required privileges."""
    def decorator(f):
        @wraps(f)
        def decorated_function(username, *args, **kwargs):
            hacker = Hacker.findOne(username=username, excludes=["password"])
            if not hacker:
                raise Unauthorized()
            if not any(True for r in hacker.privileges if r in roles):
                raise Forbidden()
            return f(username, *args, **kwargs)
        return decorated_function
    return decorator
