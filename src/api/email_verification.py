# -*- coding: utf-8 -*-
"""
    src.api.email_verification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions:

        check_verification_status()
        update_verification_status()

"""
from flask import request, redirect, current_app as app
from src.api import Blueprint
from werkzeug.exceptions import NotFound, BadRequest
from src.models.hacker import Hacker
from src import bcrypt
from src.common.decorators import authenticate


email_verify_blueprint = Blueprint("email_verification", __name__)


@email_verify_blueprint.get("/email/verify/<email>/")
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
        401:
            description: Unauthorized
        404:
            description: No Hacker exists with that email!
    """

    hacker = Hacker.objects(email=email).only("email_verification").first()

    if not hacker:
        return NotFound()

    res = {
        "email_status": hacker.email_verification
    }

    return res, 200


@email_verify_blueprint.get("/email/verify/")
def update_registration_status():
    """
    Updates the email registration status
    ---
    tags:
        - email
    parameters:
        - name: token
          in: query
          schema:
            type: string
          required: true
    responses:
        200:
            description: OK
        404:
            description: No Hacker exists with that email!
        5XX:
            description: Unexpected error.
    """
    email_token = request.args.get("token", "")
    redirect_uri = app.config.get("FRONTEND_URL")

    if not email_token:
        raise BadRequest("No email token was provided")

    hacker_email = Hacker.decode_email_token(email_token)
    hacker = Hacker.objects(email=hacker_email).first()

    if not hacker or not hacker.email_token_hash:
        raise NotFound("Invalid verification token. Please try again.")

    isvalid = bcrypt.check_password_hash(hacker.email_token_hash, email_token)
    if not isvalid:
        raise NotFound("Invalid verification token. Please try again.")

    hacker.modify(email_verification=True,
                  unset__email_token_hash="")
    hacker.save()

    return redirect(redirect_uri, code=302)


@email_verify_blueprint.post("/email/verify/<email>/")
@authenticate
def send_registration_email(email: str):
    """
    Sends a registration email to the hacker.
    ---
    tags:
        - email
    parameters:
        - name: email
          in: path
          schema:
            type: string
            format: email
          required: true
    responses:
        201:
            description: OK
        404:
            description: No Hacker exists with that hackername!
        5XX:
            description: Unexpected error.
    """

    hacker = Hacker.objects(email=email).first()

    if not hacker:
        raise NotFound()

    token = hacker.encode_email_token()

    from src.common.mail import send_verification_email
    send_verification_email(hacker, token)

    res = {
        "status": "success",
        "message": "Verification email successfully sent!"
    }

    return res, 201
