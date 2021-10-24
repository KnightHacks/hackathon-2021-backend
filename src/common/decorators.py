# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

"""
from flask import current_app as app, json, _request_ctx_stack
from functools import wraps
from werkzeug.exceptions import Unauthorized, Forbidden
from src.models.user import User
from src.common.utils import _get_token_auth_header
from six.moves.urllib.request import urlopen
from jose import jwt
from src.common.scopes import Scopes


def authenticate(f):
    """
    Authenticates the user using bearer token.
    """

    doc = getattr(f, "__doc__")
    if doc:
        setattr(f, "__doc__", doc + """security:
        - BearerAuth: []""")

    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            token = _get_token_auth_header()
            jsonurl = urlopen("https://login.microsoftonline.com/" +
                              app.config.get("AZURE_TENANT_ID") +
                              "/discovery/v2.0/keys")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
        except Exception:
            raise Unauthorized("Unable to parse authentication")

        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=["RS256"],
                    audience=app.config.get("AZURE_API_AUDIENCE"),
                    issuer=("https://sts.windows.net/" +
                            app.config.get("AZURE_TENANT_ID") +
                            "/")
                )
            except jwt.ExpiredSignatureError:
                raise Unauthorized("Token is expired")

            except jwt.JWTClaimsError:
                raise Unauthorized("Incorrect claims please check the audience"
                                   " and issuer")

            except Exception:
                raise Unauthorized("Unable to parse authentication token")

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise Unauthorized("Unable to find appropriate key")

    return decorator


def requires_scope(scope: Scopes):

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cu = _request_ctx_stack.top.current_user

            s = Scopes(cu.get("roles"))

            """ Check if the user has the required scope(s) """
            if not(scope & s):
                raise Forbidden()

            return f(*args, **kwargs)
        return decorated_function
    return decorator
