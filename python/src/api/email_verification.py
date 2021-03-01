# -*- coding: utf-8 -*-
"""
    src.api.email_verification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions:

        check_verification_status()
        update_verification_status()

"""
from flask import Blueprint
from werkzeug.exceptions import NotFound
from src.models.user import User
from src import bcrypt


email_verify_blueprint = Blueprint("email_verification", __name__)


@email_verify_blueprint.route("/email/verify/<email>/", methods=["GET"])
def check_verification_status(email: str):
    """
    Checks the email verification status
    ---
    tags:
        - email
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

    user = User.objects(email=email).only("email_verification").first()

    if not user:
        return NotFound()

    res = {
        "email_status": user.email_verification
    }

    return res, 200


"""Inline comment on following decorator is to disable flake8 'longline' err"""


@email_verify_blueprint.route("/email/verify/<email_token>/", methods=["PUT"])  # noqa: E501
def update_registration_status(email_token: str):
    """
    Updates the email registration status
    ---
    tags:
        - email
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
    user = User.objects(username=user_username).first()

    if not user or not user.email_token_hash:
        raise NotFound("Invalid verification token. Please try again.")

    isvalid = bcrypt.check_password_hash(user.email_token_hash, email_token)
    if not isvalid:
        raise NotFound("Invalid verification token. Please try again.")

    user.modify(email_verification=True,
                unset__email_token_hash="")
    user.save()

    res = {
        "status": "success",
        "message": "User email successfully verified"
    }

    return res, 200


"""Inline comment on following decorator is to disable flake8 'longline' err"""


@email_verify_blueprint.route("/email/verify/<username>/", methods=["POST"])  # noqa: E501
def send_registration_email(username: str):
    """
    Sends a registration email to the user.
    ---
    tags:
        - email
    parameters:
        - name: username
          in: path
          schema:
            type: string
          required: true
    responses:
        201:
            description: OK
        404:
            description: No User exists with that username!
        5XX:
            description: Unexpected error.
    """

    user = User.objects(username=username).first()

    if not user:
        raise NotFound()

    token = user.encode_email_token()

    from src.common.mail import send_verification_email
    send_verification_email(user, token)

    res = {
        "status": "success",
        "message": "Verification email successfully sent!"
    }

    return res, 201
