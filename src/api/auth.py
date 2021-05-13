# -*- coding: utf-8 -*-
"""
    src.api.auth
    ~~~~~~~~~~~~

"""
from flask import request, make_response, redirect, json, current_app as app
from src.api import Blueprint
from werkzeug.exceptions import BadRequest, Forbidden, NotFound, Conflict
from mongoengine.errors import NotUniqueError
from src.models.user import User
from src import bcrypt
from src.common.decorators import authenticate
import requests

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
    res.set_cookie("sid", auth_token)

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


@auth_blueprint.get("/auth/connect_discord/")
@authenticate
def connect_discord(user):
    """
    Connects the User's Discord Account.
    ---
    tags:
        - auth
    parameters:
        - in: query
          name: code
          schema:
            type: string
          required: true
    response:
        default:
            description: OK
    """
    args = request.args

    if "code" not in args:
        raise BadRequest()

    t = requests.post(
        app.config.get("DISCORD_API_URL") + "/oauth2/token",
        data={
            "code": args["code"],
            "grant_type": "authorization_code",
            "client_id": app.config.get("DISCORD_CLIENT_ID"),
            "client_secret": app.config.get("DISCORD_CLIENT_SECRET"),
            "redirect_url": app.config.get("DISCORD_REDIRECT_URL")
        }
    )

    access_token = json.loads(t.data.decode()).get("access_token")

    r = requests.get(
        app.config.get("DISCORD_API_URL") + "/users/@me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    discord_id = json.loads(r.data.decode()).get("id")

    try:
        user.update(discord_id=discord_id)
    except NotUniqueError:
        raise Conflict(
            "You can only have your discord account connected once."
        )

    return redirect("https://knighthacks.org/", code=301)
