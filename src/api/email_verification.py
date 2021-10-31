# -*- coding: utf-8 -*-
"""
    src.api.email_verification
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Functions:

        check_verification_status()
        update_verification_status()

"""
from src.api import Blueprint
from werkzeug.exceptions import Gone
from src.common.decorators import authenticate, requires_scope
from src.common.scope import Scope


email_verify_blueprint = Blueprint("email_verification", __name__)


@email_verify_blueprint.get("/email/verify/<email>/")
def check_verification_status(email: str):
    """
    Checks the email verification status
    ---
    deprecated: true
    description: >
        Deprecated, all calls to this endpoint will result in a 410 (Gone)!
    tags:
        - email
    parameters:
        - name: email
          in: path
          schema:
            type: string
          required: true
    responses:
        410:
            description: Gone
        200:
            description: OK
        401:
            description: Unauthorized
        404:
            description: No Hacker exists with that email!
    """

    raise Gone("Hacker emails are no longer being verified.")


@email_verify_blueprint.get("/email/verify/")
def update_registration_status():
    """
    Updates the email registration status
    ---
    deprecated: true
    description: >
        Deprecated, all calls to this endpoint will result in a 410 (Gone)!
    tags:
        - email
    parameters:
        - name: token
          in: query
          schema:
            type: string
          required: true
    responses:
        410:
            description: Gone
        200:
            description: OK
        404:
            description: No Hacker exists with that email!
        5XX:
            description: Unexpected error.
    """

    raise Gone("Hacker emails are no longer being verified. "
               "If you have arrived here after clicking the link "
               "in your email, you don't need to do anything and "
               "you may safely close this window. "
               "If you have any questions or are experiencing "
               "any issues, please contact us at team@knighthacks.org")


@email_verify_blueprint.post("/email/verify/<email>/")
@authenticate
@requires_scope(Scope.Email_Send)
def send_registration_email(email: str):
    """
    Sends a registration email to the hacker.
    ---
    deprecated: true
    description: >
        Deprecated, all calls to this endpoint will result in a 410 (Gone)!
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
        410:
            description: Gone
        201:
            description: OK
        404:
            description: No Hacker exists with that hackername!
        5XX:
            description: Unexpected error.
    """

    raise Gone("Hacker emails are no longer being verified.")
