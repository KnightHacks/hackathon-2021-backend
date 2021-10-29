# -*- coding: utf-8 -*-
"""
    src.api.auth
    ~~~~~~~~~~~~

"""
from flask import current_app as app
from src.api import Blueprint
from src.common.decorators import authenticate
from src.common.utils import current_user

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.get("/auth/me")
@authenticate
def me():
    """
    Returns the currently authenticated user's information
    ---
    tags:
        - auth
    responses:
        201:
            description: ok
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            roles:
                                type: array
                                items:
                                    type: string
                                    description: Application roles
    """

    roles = current_user

    app.logger.debug(roles)

    return {"roles": roles.get("roles", [])}, 200
