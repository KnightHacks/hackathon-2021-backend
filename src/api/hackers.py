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
from src.models.resume import Resume
from src.common.decorators import authenticate
from json import JSONDecodeError
from datetime import datetime, timedelta


hackers_blueprint = Blueprint("hackers", __name__)


@hackers_blueprint.post("/hackers/resume/")
def create_hacker_resume():
    """
    Creates a hacker resume
    ---
    tags:
        - hacker
    summary: Creates a new resume for a Hacker. Only accepts pdfs.
    description: Creates a new resume for a Hacker. Only accepts pdfs.
    requestBody:
        content:
            multipart/form-data:
                schema:
                    type: object
                    required:
                        - resume
                    properties:
                        resume:
                            type: string
                            format: binary
                encoding:
                    resume:
                        contentType: application/pdf
    responses:
        201:
            description: OK
            headers:
                Expires:
                    description: >
                        The date/time that the uploaded resume is
                        deleted from the server.
                    schema:
                        type: string
                        format: date-time
                        example: 2021-09-20T00:00:00Z
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            id:
                                type: string
        415:
            description: Unsupported Media Type, endpoint only accepts pdfs
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            id:
                                type: string
    links:
        createHacker:
            operationId: create_hacker
            requestBody:
                content:
                    application/json:
                        schema:
                            allOf:
                                - $ref: '#/paths/~1api~1hackers~1/requestBody/content/application~1json/schema' # noqa: E501
                                - type: object
                                  properties:
                                    resume_id: '$response.body#/id'
            description: >
                The `id` value returned in the response can be used as the `resume_id` in `POST /hackers/`
    """
    file = request.files["resume"]

    if file.mimetype != "application/pdf":
        raise UnsupportedMediaType(
            "Unsupported Media Type. Endpoint only accepts PDFs"
        )

    resume = Resume()

    resume.file.put(file, content_type="application/pdf")

    resume.save()

    res = make_response({"id": resume.id})
    expTime = datetime.utcnow() + timedelta(hours=24)
    res.headers["Expires"] = expTime.isoformat() + "Z"

    return res, 201


@hackers_blueprint.post("/hackers/")
def create_hacker():
    """
    Creates a new Hacker.
    ---
    tags:
        - hacker
    summary: Create Hacker
    operationId: create_hacker
    requestBody:
        content:
            application/json:
                schema:
                    allOf:
                        - $ref: '#/components/schemas/Hacker'
                        - type: object
                          properties:
                            isaccepted:
                                readOnly: true
                            rsvp_status:
                                readOnly: true
                            resume_id:
                                type: string
            multipart/form-data:
                schema:
                    type: object
                    properties:
                        hacker:
                            deprecated: true
                            allOf:
                                - $ref: '#/components/schemas/Hacker'
                                - type: object
                                  description: >
                                    Deprecated,
                                    do not use `multipart/form-data`,
                                    use `application/json`
                                    and upload the resume through the
                                    `/api/hackers/resume/` POST endpoint.
                                  properties:
                                    isaccepted:
                                        readOnly: true
                                    rsvp_status:
                                        readOnly: true
                        resume:
                             deprecated: true
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
        404:
            description: A resume with the provided id does not exist.
        409:
            description: Sorry, that email already exists.
        5XX:
            description: Unexpected error.
    """
    if request.content_type == "multipart/form-data":
        try:
            data = json.loads(request.form.get("hacker"))
        except JSONDecodeError:
            raise BadRequest("Invalid JSON sent in hacker form part.")
    elif request.content_type == "application/json":
        data = request.get_json()
    else:
        raise UnsupportedMediaType()

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

    if "resume_id" in data:
        try:
            resume_doc = Resume.objects.get_or_404(id=data["resume_id"])
        except ValidationError:
            raise BadRequest(f"{data['resume_id']} is not a valid ObjectId.")
    elif resume:
        resume_doc = Resume(attached=True)
    else:
        resume_doc = None

    try:
        hacker = Hacker.createOne(**data)

        if resume and resume_doc:
            hacker.resume = resume_doc

            hacker.resume.file.put(resume, content_type="application/pdf")

            hacker.resume.save()
        elif "resume_id" in data and resume_doc:
            hacker.resume = resume_doc

            hacker.resume.attached = True

            hacker.resume.save()

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

    res = make_response(res)
    res.headers["Deprecation"] = (
        "The use of multipart/form-data is deprecated,"
        " use `application/json` and upload the resume through the "
        "/api/hackers/resume/ POST endpoint.")

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

    resume = hacker.resume.file.read()

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
