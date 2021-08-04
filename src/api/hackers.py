# -*- coding: utf-8 -*-
"""
    src.api.hackers
    ~~~~~~~~~~~~~~~

    Functions:

        create_hacker()

"""
from flask import request, make_response, json
from src.api import Blueprint
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import (
    BadRequest,
    Conflict,
    NotFound,
    Unauthorized,
    UnsupportedMediaType
)
from src.models.hacker import Hacker
from src.models.user import ROLES
from src.common.decorators import authenticate, privileges


hackers_blueprint = Blueprint("hackers", __name__)


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
            multipart/form-data:
                schema:
                    type: object
                    properties:
                        hacker:
                            $ref: '#/components/schemas/Hacker'
                        resume:
                             type: string
                             format: binary
                encoding:
                    hacker:
                        contentType: application/json
                    resume:
                        contentType: application/pdf
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
    data = json.loads(request.form.get("hacker"))
    resume = None

    if "roles" in data:
        del data["roles"]

    if "date" in data:
        del data["date"]

    if "email_verification" in data:
        del data["email_verification"]

    if "email_token_hash" in data:
        del data["email_token_hash"]

    if not data:
        raise BadRequest()

    if "resume" in request.files:
        resume = request.files["resume"]

        if resume.content_type != "application/pdf":
            raise UnsupportedMediaType()

    try:
        hacker = Hacker(**data, roles=ROLES.HACKER)

        if resume:
            hacker.resume.put(resume, content_type="application/pdf")

        hacker.save()

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


@hackers_blueprint.get("/hackers/<username>/resume/")
def get_hacker_resume(username: str):
    """
    Get Hacker Resume
    ---
    tags:
        - hacker
    parameters:
        - name: username
          in: path
          schema:
              type: string
          description: The hacker's username
          required: true
    responses:
        200:
            content:
                application/pdf:
                    schema:
                        type: string
                        format: binary
    """

    hacker = Hacker.objects(
        username=username
    ).exclude(*Hacker.private_fields).first()

    if not hacker:
        raise NotFound("A hacker with that username does not exist")

    if not hacker.resume:
        raise NotFound("There is no resume for this hacker")

    resume = hacker.resume.read()

    res = make_response(resume)
    res.headers["Content-Type"] = "application/pdf"

    return res


@hackers_blueprint.get("/hackers/<username>/")
def get_hacker_search(username: str):
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
    hacker = Hacker.objects(username=username).exclude(
        *Hacker.private_fields).first()

    if not hacker:
        raise NotFound()

    res = {
        "Hacker Profile": hacker,
        "User Name": hacker.username,
        "message": "Successfully reached profile.",
        "status": "success"
    }

    return res, 200


@hackers_blueprint.delete("/hackers/<username>/")
@authenticate
@privileges(ROLES.HACKER | ROLES.MOD | ROLES.ADMIN)
def delete_hacker(loggedin_user, username: str):
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
        401:
            description: Unauthorized
        404:
            description: Specified hacker does not exist.
        5XX:
            description: Unexpected error.
    """

    if (not(ROLES(loggedin_user.roles) & (ROLES.MOD | ROLES.ADMIN))
            and loggedin_user.username != username):
        raise Unauthorized("Hacker can only delete their own account!")

    hacker = Hacker.objects(username=username)

    if not hacker:
        raise NotFound("The specified hacker does not exist in the database.")
    hacker.delete()

    res = {
        "status": "success",
        "message": "Hacker was deleted!"
    }

    return res, 201


@hackers_blueprint.put("/hackers/<username>/")
def update_user_profile_settings(username: str):
    """
    Updates hacker profile settings
    ---
    tags:
        - hacker
    summary: Updates user profile settings
    parameters:
        - id: username
          in: path
          description: user name
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Hacker'
    responses:
        201:
            description: OK
        400:
            description: Bad Request
        404:
            description: Group doesn't exist
        5XX:
            description: Unexpected error.
    """
    update = request.get_json()
    if not update:
        raise BadRequest()

    hacker = Hacker.objects(username=username).first()
    if not hacker:
        raise NotFound()

    if update.get("email") is not None and update.get("email") != hacker.email:
        update["email_verification"] = False
        newemail = True
    else:
        newemail = False

    try:
        hacker.update(**update)
    except ValidationError:
        raise BadRequest()

    """Send Verification Email if New Email"""
    if newemail:
        token = hacker.encode_email_token()
        from src.common.mail import send_verification_email
        send_verification_email(hacker, token)

    res = {
        "status": "success",
        "message": "Hacker profile successfully updated"
    }

    return res, 201


@hackers_blueprint.get("/hackers/<username>/settings/")
def hacker_settings(username: str):
    """
    Gets the hacker settings
    ---
    tags:
    - hacker
    parameters:
        - id: username
          in: path
          description: user name
          required: true
          schema:
              type: string
    responses:
        200:
            content:
                application/json:
                    schema:
                        $ref: '#/components/schemas/Hacker'
        404:
            description: Hacker not found!
    """

    hacker = Hacker.objects(username=username).exclude(
        *Hacker.private_fields
    ).first()

    if not hacker:
        raise NotFound()

    hacker = hacker.to_mongo().to_dict()
    hacker.pop("_cls")

    hacker["roles"] = ROLES(hacker["roles"])

    res = {
        "hacker": hacker,
        "status": "success",
        "message": "Found hacker settings"
    }

    return res, 200


@hackers_blueprint.put("/hackers/<username>/accept/")
@authenticate
@privileges(ROLES.ADMIN)
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
    hackers = Hacker.objects().exclude(*Hacker.private_fields)

    if not hackers:
        raise NotFound("There are no hackers created.")

    res = {
        "hackers": hackers,
        "status": "success"
    }

    return res, 201
