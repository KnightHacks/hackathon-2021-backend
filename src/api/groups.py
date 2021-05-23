# -*- coding: utf-8 -*-
"""
    src.api.groups
    ~~~~~~~~~~~~~~

    Functions:

        create_group()
        edit_group()

"""
from flask import request
from src.api import Blueprint
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from src.models.hacker import Hacker
from src.models.group import Group


groups_blueprint = Blueprint("groups", __name__)


@groups_blueprint.post("/groups/")
def create_group():
    """
    Creates a group
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


@groups_blueprint.put("/groups/<group_name>/")
def edit_group(group_name: str):
    """
    Updates a Group
    ---
    tags:
        - groups
    summary: Updates a Group
    parameters:
        - id: group_name
          in: path
          description: The name of the group to be updated.
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Group'
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

    for k, email in enumerate(update["members"]):
        member = Hacker.objects(email=email).first()
        if not member:
            raise NotFound(description="Group Member(s) does not exist.")
        update["members"][k] = member

    group = Group.objects(name=group_name)
    if not group:
        raise NotFound()

    try:
        group.update(**update)
    except NotUniqueError:
        raise Conflict("Sorry, a group already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Group successfully updated."
    }
    return res, 201


@groups_blueprint.get("/groups/<group_name>/")
def get_group(group_name: str):
    """
    Retrieves a group's schema from their group name
    ---
    tags:
        - groups
    summary: Gets a group's schema from their group name
    parameters:
        - name: group_name
          in: path
          type: string
          description: The group's schema.
          required: true
    responses:
        200:
            description: OK

    """
    group = Group.objects(name=group_name).exclude("id").first()
    if not group:
        raise NotFound()

    group_dict = group.to_mongo().to_dict()

    members = []

    for member in group.members:

        members.append({
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "username": member.username
        })

    group_dict["members"] = members

    res = {
        "group": group_dict,
        "status": "success"
    }

    return res, 200


@groups_blueprint.get("/groups/get_all_groups/")
def get_all_groups():
    """
    Returns an array of group documents.
    ---
    tags:
        - group
    summary: returns an array of group documents
    responses:
        200:
            description: OK
        404:
            description: No group documents are created.
        5XX:
            description: Unexpected error (the API issue).
    """
    groups = Group.objects()

    if not groups:
        raise NotFound("There are no groups created.")

    res = {
        "groups": groups,
        "status": "success"
    }

    return res, 200
