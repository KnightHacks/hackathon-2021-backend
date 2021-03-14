# -*- coding: utf-8 -*-
"""
    src.api.sponsor
    ~~~~~~~~~~~~~~~

    Functions:

        create_sponsor()
        update_sponsor()

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized
from src.models.sponsor import Sponsor
from src.models.user import ROLES
from src.common.decorators import authenticate, privileges

sponsors_blueprint = Blueprint("sponsors", __name__)


@sponsors_blueprint.route("/sponsors/", methods=["POST"])
def create_sponsor():
    """
    Creates a new Sponsor.
    ---
    tags:
        - sponsor
    summary: Create Sponsor
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Sponsor'
        description: Created Sponsor Object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        409:
            description: Sorry, that sponsor_name already exists.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data:
        raise BadRequest("Not data")

    try:
        sponsor = Sponsor.createOne(**data, roles=ROLES.SPONSOR)
    except NotUniqueError:
        raise Conflict("Sorry, this sponsor already exists.")
    except ValidationError:
        raise BadRequest("Validation Error")

    """Send Verification Email"""
    token = sponsor.encode_email_token()
    from src.common.mail import send_verification_email
    send_verification_email(sponsor, token)

    res = {
        "status": "success",
        "message": "Sponsor was created!"
    }

    return res, 201


@sponsors_blueprint.route("/sponsors/delete_sponsor/<sponsor_name>/", methods=["DELETE"])  # noqa: E501
@authenticate
@privileges(ROLES.SPONSOR | ROLES.ADMIN)
def delete_sponsor(loggedin_user, sponsor_name: str):
    """
    Deletes an existing Sponsor.
    ---
    tags:
        - sponsor
    summary: Delete Sponsor
    parameters:
        - id: sponsor_name
          in: path
          description: Sponsor name
          required: true
          schema:
            type: string
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        409:
            description: Sorry, that sponsor_name already exists.
        5XX:
            description: Unexpected error.
    """

    if (not(ROLES(loggedin_user.roles) & (ROLES.MOD | ROLES.ADMIN))
            and loggedin_user.sponsor_name != sponsor_name):
        raise Unauthorized("Sponsor can only delete their own account!")

    sponsor = Sponsor.objects(sponsor_name=sponsor_name)

    if not sponsor:
        raise NotFound("The specified sponsor does not exist in the database.")

    sponsor.delete()

    res = {
        "status": "success",
        "message": "Sponsor was deleted!"
    }

    return res, 201
