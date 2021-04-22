# -*- coding: utf-8 -*-
"""
    src.api.teams
    ~~~~~~~~~~~~~~

    Functions:

        create_team()
        edit_team()

"""
from flask import Blueprint, request
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound
from src.models.hacker import Hacker
from src.models.team import Team


teams_blueprint = Blueprint("teams", __name__)


@teams_blueprint.route("/teams/", methods=["POST"])
def create_team():
    """
    Creates a team
    ---
    tags:
        - teams
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Team'
        description: Created Team Object
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
            raise NotFound(description="Team Member(s) does not exist.")
        data["members"][k] = member

    try:
        Team.createOne(**data)
    except NotUniqueError:
        raise Conflict("Sorry, a team already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Team was created!"
    }

    return res, 201


@teams_blueprint.route("/teams/<team_name>/", methods=["PUT"])
def edit_team(team_name: str):
    """
    Updates a Team
    ---
    tags:
        - teams
    summary: Updates a Team
    parameters:
        - id: team_name
          in: path
          description: The name of the team to be updated.
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Team'
    responses:
        201:
            description: OK
        400:
            description: Bad Request
        404:
            description: Team doesn't exist
        5XX:
            description: Unexpected error.
    """
    update = request.get_json()
    if not update:
        raise BadRequest()

    for k, email in enumerate(update["members"]):
        member = Hacker.objects(email=email).first()
        if not member:
            raise NotFound(description="Team Member(s) does not exist.")
        update["members"][k] = member

    team = Team.objects(name=team_name)
    if not team:
        raise NotFound()

    try:
        team.update(**update)
    except NotUniqueError:
        raise Conflict("Sorry, a team already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Team successfully updated."
    }
    return res, 201


@teams_blueprint.route("/teams/<team_name>/", methods=["GET"])
def get_team(team_name: str):
    """
    Retrieves a team's schema from their team name
    ---
    tags:
        - teams
    summary: Gets a team's schema from their team name
    parameters:
        - name: team_name
          in: path
          type: string
          description: The team's schema.
          required: true
    responses:
        200:
            description: OK

    """
    team = Team.objects(name=team_name).exclude("id").first()
    if not team:
        raise NotFound()

    team_dict = team.to_mongo().to_dict()

    members = []

    for member in team.members:

        members.append({
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "username": member.username
        })

    team_dict["members"] = members

    res = {
        "team": team_dict,
        "status": "success"
    }

    return res, 200
