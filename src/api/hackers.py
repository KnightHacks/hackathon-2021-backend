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
    UnsupportedMediaType
)
from src.models.hacker import Hacker
from src.common.decorators import authenticate
from json import JSONDecodeError


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
            description: Sorry, that email already exists.
        5XX:
            description: Unexpected error.
    """
    try:
        data = json.loads(request.form.get("hacker"))
    except JSONDecodeError:
        raise BadRequest("Invalid JSON sent in hacker form part.")

    resume = None

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
        hacker = Hacker.createOne(**data)

        if resume:
            hacker.resume.put(resume, content_type="application/pdf")

        hacker.save()

    except NotUniqueError:
        raise Conflict("Sorry, that email already exists.")
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


@hackers_blueprint.get("/hackers/<email>/resume/")
@authenticate
def get_hacker_resume(email: str):
    """
    Get Hacker Resume
    ---
    tags:
        - hacker
    parameters:
        - name: email
          in: path
          schema:
              type: string
          description: The hacker's email
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
        email=email
    ).exclude(*Hacker.private_fields).first()

    if not hacker:
        raise NotFound("A hacker with that username does not exist")

    if not hacker.resume:
        raise NotFound("There is no resume for this hacker")

    resume = hacker.resume.read()

    res = make_response(resume)
    res.headers["Content-Type"] = "application/pdf"

    return res


@hackers_blueprint.put("/hackers/<email>/accept/")
@authenticate
def accept_hacker(_, email: str):
    """
    Accepts a Hacker
    ---
    tags:
        - hacker
    parameters:
        - id: email
          in: path
          description: email
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

    hacker = Hacker.objects(email=email).first()
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
@authenticate
def get_all_hackers(_):
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
