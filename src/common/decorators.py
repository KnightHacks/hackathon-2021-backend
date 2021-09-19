# -*- coding: utf-8 -*-
"""
    src.common.decorators
    ~~~~~~~~~~~~~~~~~~~~~

"""
from flask import request, current_app as app, make_response
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


def deprecated(date: str = None, alternate: str = None):
    """
    Mark an endpoint as deprecated.

    @param date iso8601 str describing when the endpoint will be unresponsive
    @param alternate alternate uri for the deprecated endpoint
    """

    def decorator(f):

        """ Mark the endpoint as deprecated in the openapi spec """
        doc = getattr(f, "__doc__")
        if doc:
            setattr(f, "__doc__", doc + "deprecated: true")

        @wraps(f)
        def decorated_function(*args, **kwargs):
            app.logger.warning(
                "Call to deprecated endpoint function: " +
                getattr(f, "__name__")
            )

            response = make_response(f(*args, **kwargs))

            response.headers["Deprecation"] = date if date else "true"

            if alternate:
                response.headers["Link"] = f"<{alternate}>; rel=\"alternate\""

            if date:
                response.headers["Sunset"] = date

            return response

        return decorated_function
    return decorator
