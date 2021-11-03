# -*- coding: utf-8 -*-
"""
    src.api.sponsors
    ~~~~~~~~~~~~~~~

    Functions:

        create_sponsor()
        get_all_sponsors

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
from src.models.sponsor import Sponsor
from src.common.decorators import authenticate, requires_scope
from src.common.scope import Scope
from json import JSONDecodeError


sponsors_blueprint = Blueprint("sponsors", __name__)


@sponsors_blueprint.post("/sponsors/")
@authenticate
@requires_scope(Scope.Sponsor_Create)
def create_sponsor():
    """
    Creates a new sponsor.
    ---
    tags:
        - sponsor
    summary: Create sponsor
    operationId: create_sponsor
    requestBody:
        content:
            application/json:
                schema:
                    allOf:
                        - $ref: '#/components/schemas/Sponsor'
                        - type: object
            multipart/form-data:
                schema:
                    type: object
                    properties:
                        sponsor:
                            deprecated: true
                            allOf:
                                - $ref: '#/components/schemas/Sponsor'
                                - type: object
                                  description: >
                                    Deprecated,
                                    do not use `multipart/form-data`,
                                    use `application/json`.
                                  properties:
                encoding:
                    sponsor:
                        contentType: application/json
        description: Created sponsor Object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        409:
            description: Sorry, that sponsor already exists.
        5XX:
            description: Unexpected error.
    """
    if "multipart/form-data" in request.content_type:
        try:
            data = json.loads(request.form.get("sponsor"))
        except JSONDecodeError:
            raise BadRequest("Invalid JSON sent in sponsor form part.")
    elif request.content_type == "application/json":
        data = request.get_json()
    else:
        raise UnsupportedMediaType()

    if not data:
        raise BadRequest()

    try:
        sponsor = Sponsor.createOne(**data)
        sponsor.save()

    except NotUniqueError:
        raise Conflict("Sorry, that sponsor already exists.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "sponsor was created!"
    }

    res = make_response(res)

    if "multipart/form-data" in request.content_type:
        res.headers["Deprecation"] = (
            "The use of multipart/form-data is deprecated. ")

    if "socials" in data:
        res.headers["Deprecation"] = (
            "The socials field is deprecated use sponsor_website instead")

    return res, 201


@sponsors_blueprint.get("/sponsors/get_all_sponsors/")
def get_all_sponsors():
    """
    Returns an array of sponsor documents.
    ---
    tags:
        - sponsor
    summary: returns an array of sponsor documents
    responses:
        200:
            description: OK
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            sponsors:
                                type: array
                                items:
                                    $ref: '#/components/schemas/Sponsor'
                            status:
                                type: string
        404:
            description: No sponsor documents are created.
        5XX:
            description: Unexpected error (the API issue).
    """
    sponsors = Sponsor.objects().exclude(*Sponsor.private_fields)

    if not sponsors:
        raise NotFound("There are no sponsors created.")

    res = {
        "sponsors": sponsors,
        "status": "success"
    }

    res = make_response(res)
    res.headers["Deprecation"] = (
        "The socials field is deprecated "
        "use sponsor_website instead."
    )

    return res, 200
