# -*- coding: utf-8 -*-
"""
    src.api.auth
    ~~~~~~~~~~~~

"""
from flask import Blueprint, request, current_app, make_response
from werkzeug.exceptions import BadRequest, Forbidden, NotFound
from src.models.user import User
from src import bcrypt
from src.common.decorators import authenticate

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth/login/", methods=["POST"])
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
    res.set_cookie("sid", auth_token)

    return res


@auth_blueprint.route("/auth/signout/", methods=["GET"])
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
