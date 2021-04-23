# -*- coding: utf-8 -*-
"""
    src.api.teams
    ~~~~~~~~~~~~~~

    Functions:

        create_team()
        edit_team()
        update_team()
        add_member()
        remove_member()
        get_team()

"""
from flask import Blueprint, request, make_response, current_app as app
from mongoengine.errors import NotUniqueError, ValidationError
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized, UnsupportedMediaType
from werkzeug.utils import secure_filename
from src.common.decorators import authenticate, privileges
from src.models.user import ROLES
from src.models.hacker import Hacker
from src.models.team import Team


teams_blueprint = Blueprint("teams", __name__)


@teams_blueprint.route("/teams/", methods=["POST"])
def create_team(hacker=None):
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

    data["pending_members"] = []

    for k, email in enumerate(data["members"]):
        member = Hacker.objects(email=email).first()
        if not member:
            raise NotFound("Team Member(s) does not exist.")
        if member.team:
            raise Conflict("Team Members cannot be in multiple teams.")

        if member is not hacker:
            pass  # TODO: Invite Hacker to team
            data["pending_members"].append(member)
            continue

        data["members"].append(member)

    try:
        created = Team.createOne(**data)
    except NotUniqueError:
        raise Conflict("Sorry, a team already exists with that name.")
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Team was created!"
    }

    return res, 201

@teams_blueprint.route("/teams/<team_name>/icon/", methods=["GET"])
def download_team_icon(team_name: str):
    team = Team.objects(name=team_name).first()

    if not team:
        raise NotFound("A team with that name does not exist")

    if not team.icon:
        raise NotFound("There is no icon for this team.")

    icon_name = team.icon_name

    res = make_response(team.icon.read())
    res.headers["Content-Type"] = "application/octet-stream"
    res.headers["Content-Disposition"] = f"attachment; filename={icon_name}"

    return res

@teams_blueprint.route("/teams/<team_name>/icon/", methods=["PUT"])
def upload_team_icon(team_name: str):
    team = Team.objects(name=team_name).first()

    if "icon" not in request.files:
        raise BadRequest()

    icon = request.files["icon"]

    if icon.content_type not in ("image/png", "image/jpeg"):
        raise UnsupportedMediaType()

    if team.icon:
        team.icon.put(icon, content_type=icon.content_type)
    else:
        team.icon.replace(icon, content_type=icon.content_type)

    team.icon_name = secure_filename(icon.filename)

    team.save()

    res = {
        "status": "success",
        "message": "Team icon was sucessfully updated!"
    }

    return res, 201


@teams_blueprint.route("/teams/<team_name>/", methods=["PUT"])
@authenticate
def edit_team(_, team_name: str):
    """
    Updates a Team
    ---
    tags:
        - teams
    summary: Updates a Team.
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
        if member.team:
            raise Conflict("Member is already in a team!")
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


@teams_blueprint.route("/teams/<team_name>/member/", methods=["PATCH"])
@authenticate
def add_member(user, team_name: str):
    """
    Adds a member to a Team
    ---
    tags:
        - teams
    summary: Adds a member to a Team, all members in a team must be a Hacker.
    parameters:
        - id: team_name
          in: path
          name: team_name
          description: The name of the team to add a member to.
          required: true
          schema:
            type: string
    requestBody:
        content:
            application/json:
                schema:
                    type: object
                    properties:
                        member:
                            type: string
                            description: A hacker's email address.
                            example: foobar@email.com
                            required: true

    responses:
        201:
            description: OK
        400:
            description: Bad Request
        404:
            description: Team or Hacker doesn't exist
        5XX:
            description: Unexpected error.

    """
    patch = request.get_json()
    if not patch or "member" not in patch:
        raise BadRequest()

    member = Hacker.objects(email=patch["member"]).first()
    if not member:
        raise NotFound(description="Team Member does not exist.")

    team = Team.objects(name=team_name).first()
    if not team:
        raise NotFound("Team does not exist.")

    if member in team.members:
        raise Conflict("Member is already in this team!")
    if member.team:
        raise Conflict("Member is already in a team!")

    if (user in team.members
            and not user.roles & ROLES.ADMIN):
        raise Unauthorized()

    try:
        team.update(add_to_set__members=[member])
    except ValidationError:
        raise BadRequest("Invalid email provided for Member.")

    res = {
        "status": "success",
        "message": "Team member added successfully."
    }
    return res, 201


@teams_blueprint.route("/teams/<team_name>/member/<email>/", methods=["DELETE"])
@authenticate
def remove_member(user, team_name: str, email: str):
    """
    Removes a member from a Team
    ---
    tags:
        - teams
    summary: Removes a member from a Team.
    parameters:
        - id: team_name
          in: path
          name: team_name
          description: The name of the team to remove a member from.
          required: true
          schema:
            type: string
        - id: email
          in: path
          name: email
          description: A hacker's email address.
          example: foobar@email.com
          required: true
          schema:
            type: string
    responses:
        201:
            description: OK
        400:
            description: Bad Request
        404:
            description: Team or Hacker doesn't exist
        5XX:
            description: Unexpected error.

    """
    patch = request.args
    if not patch or "email" not in patch:
        raise BadRequest()

    member = Hacker.objects(email=patch["email"]).first()
    if not member:
        raise NotFound("Team Member does not exist.")

    team = Team.objects(name=team_name).first()
    if not team:
        raise NotFound("Team does not exist.")

    if member not in team.members:
        raise NotFound("Team member does not exist in team.")

    if (user in team.members
            and not user.roles & ROLES.ADMIN):
        raise Unauthorized()

    team.update(pull__members=member)

    res = {
        "status": "success",
        "message": "Team member removed successfully."
    }
    return res, 201


@teams_blueprint.route("/teams/<team_name>/", methods=["DELETE"])
@authenticate
def delete_team(user, team_name: str):
    """
    Deletes a team
    ---
    tags:
        - teams
    summary: Deletes a team
    parameters:
        - name: team_name
          in: path
          schema:
              type: string
          description: The team's name
          required: true
    responses:
        201:
            description: OK
        404:
            description: Team does not exist
        5XX:
            description: Unexpected error
    """
    team = Team.objects(name=team_name).first()

    if (user not in team or not user.roles & ROLES.ADMIN):
        raise Unauthorized()

    team.delete()

    res = {
        "status": "success",
        "message": "Team deleted successfully."
    }
    return res, 201


@teams_blueprint.route("/teams/<team_name>/", methods=["GET"])
@authenticate
def get_team(user, team_name: str):
    """
    Retrieves a team's schema from their team name
    ---
    tags:
        - teams
    summary: Gets a team's schema from their team name
    parameters:
        - name: team_name
          in: path
          schema:
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
