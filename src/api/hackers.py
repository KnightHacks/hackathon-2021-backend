# -*- coding: utf-8 -*-
"""
    src.api.hackers
    ~~~~~~~~~~~~~~~

    Functions:

        create_hacker()

    Variables:

        HACKER_PROFILE_FIELDS

"""
from flask import request
from src.api import Blueprint
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized
import dateutil.parser
from src.models.hacker import Hacker


hackers_blueprint = Blueprint("hackers", __name__)

HACKER_PROFILE_FIELDS = ("resume", "socials", "school_name", "grad_year")


@hackers_blueprint.post("/hackers/")
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

    if data.get("date"):
        data["date"] = dateutil.parser.parse(data["date"])

    data["hacker_profile"] = {}
    for f in HACKER_PROFILE_FIELDS:
        data["hacker_profile"][f] = data.pop(f, None)

    try:
        hacker = Hacker.createOne(**data)

    except NotUniqueError:
        raise Conflict("Sorry, that username or email already exists.")
    except ValidationError:
        raise BadRequest()

    """Send Verification Email"""
    token = hacker.encode_email_token()
    from src.common.mail import send_verification_email
    send_verification_email(hacker, token)

    res = {
        "status": "success",
        "message": "Hacker was created!"
    }

    return res, 201


@hackers_blueprint.get("/hackers/<username>/")
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
          schema:
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

@hackers_blueprint.put("/hackers/<username>/accept/")
def accept_hacker(_, username: str):
    """
    Accepts a Hacker
    ---
    tags:
        - hacker
    parameters:
        - id: username
          in: path
          description: username
          required: true
          schema:
            type: string
    responses:
        201:
            description: OK
        404:
            description: Hacker does not exist.
        5XX:
            description: Unexpected error.
    """

    hacker = Hacker.objects(username=username).first()
    if not hacker:
        raise NotFound()

    hacker.update(isaccepted=True)

    """Send Acceptance Email"""
    from src.common.mail import send_hacker_acceptance_email
    send_hacker_acceptance_email(hacker)

    res = {
        "status": "success",
        "message": "Hacker has been accepted!"
    }

    return res, 201


@hackers_blueprint.get("/hackers/get_all_hackers/")
def get_all_hackers():
    """
    Returns an array of hacker documents.
    ---
    tags:
        - hacker
    summary: returns an array of hacker documents
    responses:
        201:
            description: OK
        404:
            description: No hacker documents are created.
        5XX:
            description: Unexpected error (the API issue).
    """
    hackers = Hacker.objects()

    if not hackers:
        raise NotFound("There are no hackers created.")

    res = {
        "hackers": hackers,
        "status": "success"
    }

    return res, 201
