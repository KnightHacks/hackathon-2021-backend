# -*- coding: utf-8 -*-
"""
    src.api.auth
    ~~~~~~~~~~~~

"""
from flask import request, make_response
from src.api import Blueprint
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from src.models.user import User
from src import bcrypt
from src.common.decorators import authenticate

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.post("/auth/login/")
def login():
    """
    Logs in User
    ---
    tags:
        - auth
    requestBody:
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        username:
                            type: string
                        password:
                            type: string
    responses:
        200:
            description: OK
            headers:
                Set-Cookie:
                    description: JWT token to save session data.
                    schema:
                        type: string
        400:
            description: Login failed.
        404:
            description: User not found.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data:
        raise BadRequest()

    if not data.get("password") and not data.get("username"):
        raise BadRequest()

    user = User.objects(username=data["username"]).first()
    if not user:
        raise NotFound()

    if not bcrypt.check_password_hash(user.password, data["password"]):
        raise Forbidden()

    auth_token = user.encode_auth_token()

    res = make_response()
    res.set_cookie("sid", auth_token, samesite="None")

    return res


@auth_blueprint.get("/auth/signout/")
@authenticate
def logout(_):
    """
    Logs out the user.
    ---
    tags:
        - auth
    response:
        default:
            description: OK
    """

    res = make_response()
    res.delete_cookie("sid")

    return res
