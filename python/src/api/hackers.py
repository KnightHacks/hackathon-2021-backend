# -*- coding: utf-8 -*-
"""
    src.api.hackers
    ~~~~~~~~~~~~~~~

    Functions:

        create_hacker()

    Variables:

        HACKER_PROFILE_FIELDS

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound
import dateutil.parser
from src.models.hacker import Hacker


hackers_blueprint = Blueprint("hackers", __name__)

HACKER_PROFILE_FIELDS = ("resume", "socials", "school_name", "grad_year")


@hackers_blueprint.route("/hackers/", methods=["POST"])
def create_hacker():
    """
    Creates a new Hacker.
    ---
    tags:
        - hacker
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
    data = request.get_json()

    if not data:
        raise BadRequest()

    if data["date"]:
        data["date"] = dateutil.parser.parse(data["date"])

    data["hacker_profile"] = {}
    for f in HACKER_PROFILE_FIELDS:
        data["hacker_profile"][f] = data.pop(f, None)

    try:
        Hacker.createOne(**data, roles=("HACKER",))
    except NotUniqueError:
        raise Conflict("Sorry, that username or email already exists.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Hacker was created!"
    }

    return res, 201


@hackers_blueprint.route("/hackers/<username>/", methods=["GET"])
def get_user_search(username: str):
    """
    Retrieves a hacker's profile using their username.
    ---
    tags:
        - hacker
    summary: Gets a hacker's profile from their username.
    parameters:
        - name: username
          in: path
          type: string
          description: The hacker's profile.
          required: true
    responses:
        200:
            description: OK

    """
    hacker = Hacker.objects(username=username).first()
    if not hacker:
        raise NotFound()

    res = {
        "Hacker Profile": hacker.hacker_profile,
        "User Name": hacker.username,
        "message": "Successfully reached profile.",
        "status": "success"
    }

    return res, 200


@hackers_blueprint.route("/hackers/<username>/", methods=["DELETE"])
def delete_hacker(username: str):
    """
    Deletes an existing Hacker.
    ---
    tags:
        - hacker
    summary: Delete Hacker
    parameters:
        - id: username
          in: path
          description: User name
          required: true
          schema:
            type: string
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        404:
            description: Specified hacker does not exist.
        5XX:
            description: Unexpected error.
    """

    hacker = Hacker.objects(username=username)

    if not hacker:
        raise NotFound("The specified hacker does not exist in the database.")
    hacker.delete()

    res = {
        "status": "success",
        "message": "Hacker was deleted!"
    }

    return res, 201
