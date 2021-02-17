# -*- coding: utf-8 -*-
"""
    src.api.groups
    ~~~~~~~~~~~~~~

    Functions:

        create_group()
        edit_group()

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from src.models.hacker import Hacker
from src.models.group import Group


groups_blueprint = Blueprint("groups", __name__)


@groups_blueprint.route("/groups/", methods=["POST"])
def create_group():
    """
    Returns the Amount of Users
    ---
    tags:
        - groups
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Group'
        description: Created Group Object
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

    for k, email in enumerate(data["members"]):
        member = Hacker.objects(email=email).first()
        if not member:
            raise NotFound(description="Group Member(s) does not exist.")
        data["members"][k] = member

    try:
        Group.createOne(**data)
    except NotUniqueError:
        raise Conflict("Sorry, a group already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Group was created!"
    }

    return res, 201
