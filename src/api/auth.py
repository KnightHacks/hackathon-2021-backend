# -*- coding: utf-8 -*-
"""
    src.api.auth
    ~~~~~~~~~~~~

"""
from flask import current_app as app, session, redirect
from src import oauth
from src.api import Blueprint
from src.common.decorators import authenticate
from src.common.utils import current_user

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/auth/login")
def login():
    # redirect_uri = url_for("auth.getAToken", _external=True)
    redirect_uri = "http://localhost:8080/popup.html"
    res = oauth.azure.authorize_redirect(redirect_uri)
    loc = res.headers.get("Location")
    return {"loc": loc}, 200


@auth_blueprint.route("/auth/getAToken")
def getAToken():
    token = oauth.azure.authorize_access_token()

    session["token"] = token

    app.logger.debug(token)

    return redirect(f"http://localhost:8080/popup.html?t={token}")


@auth_blueprint.get("/echo")
@authenticate
def echo():

    # token = session.get("token")

    # claims = oauth.azure.parse_id_token(token)

    # roles = claims.get("roles")

    roles = current_user

    app.logger.debug(roles)

    return {"roles": roles.get("roles", [])}, 200, [("Access-Control-Allow-Origin", "http://localhost:3000")]
