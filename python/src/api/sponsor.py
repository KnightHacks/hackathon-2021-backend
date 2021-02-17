#TODO
# -*- coding: utf-8 -*-
"""
    src.api.hackers
    ~~~~~~~~~~~~~~~

    Functions:

        create_hacker()

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict
import dateutil.parser
from src.models.sponsor import Sponsor

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
        raise BadRequest()

    try:
        Sponsor.createOne(**data, roles=("SPONSOR",))
    except NotUniqueError:
        raise Conflict("Sorry, this sponsor already exists.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Sponsor was created!"
    }

    return res, 201