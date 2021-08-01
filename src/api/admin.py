# -*- coding: utf-8 -*-
"""
    src.api.admin
    ~~~~~~~~~~~~~~~

    Functions:

        create_hacker()
        create_sponsor()

"""
from flask import request, current_app as app
from src.api import Blueprint
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized
import dateutil.parser
from src.models.hacker import Hacker
from src.models.sponsor import Sponsor
from src.common.decorators import authenticate

HACKER_PROFILE_FIELDS = ("resume", "socials", "school_name", "grad_year")

admin_blueprint = Blueprint("admin", __name__)


@admin_blueprint.post("/admin/hackers/")
@authenticate
def create_hacker(loggedin_user):
    """
    Creates a new Hacker manually and bypasses email verification.
    ---
    tags:
        - admin
    summary: Create Hacker
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Hacker'
        description: Created Hacker Object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        409:
            description: Sorry, that username or email already exists.
        5XX:
            description: Unexpected error.
    """
    if (not(ROLES(loggedin_user.roles) & (ROLES.ADMIN))):
        raise Unauthorized("Only administrators can perform this action.")

    data = request.get_json()

    if not data:
        raise BadRequest()

    if data.get("date"):
        data["date"] = dateutil.parser.parse(data["date"])

    data["hacker_profile"] = {}
    for f in HACKER_PROFILE_FIELDS:
        data["hacker_profile"][f] = data.pop(f, None)

    try:
        Hacker.createOne(**data, roles=ROLES.HACKER, isaccepted=True,
                         email_verification=True)

    except NotUniqueError:
        raise Conflict("Sorry, that username or email already exists.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Hacker was created!"
    }

    return res, 201


@admin_blueprint.post("/admin/sponsors/")
@authenticate
def create_sponsor(loggedin_user):
    """
    Creates a new Sponsor manually and bypasses email verification.
    ---
    tags:
        - admin
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
    if (not(ROLES(loggedin_user.roles) & (ROLES.ADMIN))):
        raise Unauthorized("Only administrators can perform this action.")

    data = request.get_json()

    if not data:
        raise BadRequest("Not data")

    from src import bcrypt
    data["password"] = bcrypt.generate_password_hash(
        data["password"],
        app.config["BCRYPT_LOG_ROUNDS"])

    try:
        Sponsor.createOne(**data, roles=ROLES.SPONSOR,
                          email_verification=True)
    except NotUniqueError:
        raise Conflict("Sorry, this sponsor already exists.")
    except ValidationError:
        raise BadRequest("Validation Error")

    res = {
        "status": "success",
        "message": "Sponsor was created!"
    }

    return res, 201
