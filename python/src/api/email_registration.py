# -*- coding: utf-8 -*-
"""
    src.api.email_registration
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions:

        check_registration_status()
        update_registration_status()

"""
from flask import Blueprint
from werkzeug.exceptions import NotFound
from src.models.User import User


email_reg_blueprint = Blueprint("email_registration", __name__)


@email_reg_blueprint.route("/email_registration/<email>/", methods=["GET"])
def check_registration_status(email: str):
    """
    Checks the email registration status
    ---
    tags:
        - email_registration
    parameters:
        - name: email
          in: path
          schema:
            type: string
          required: true
    responses:
        200:
            description: OK
        404:
            description: No User exists with that email!
    """

    user = User.objects(email=email).only("email_registration").first()

    if not user:
        return NotFound()

    res = {
        "email_status": user.email_registration
    }

    return res, 200


@email_reg_blueprint.route("/email_registration/<email_token>/", methods=["PUT"])  # noqa: E501
def update_registration_status(email_token: str):
    """
    Checks the email registration status
    ---
    tags:
        - email_registration
    parameters:
        - name: email_token
          in: path
          schema:
            type: string
          required: true
    responses:
        200:
            description: OK
        404:
            description: No User exists with that email!
        5XX:
            description: Unexpected error.
    """
    user_username = User.decode_email_token(email_token)
    user = User.objects(id=user_username).first()

    if not user:
        raise NotFound()

    user.update(email_registration=True)

    res = {
        "status": "success",
        "message": "User email successfully verified"
    }

    return res, 200
