# -*- coding: utf-8 -*-
"""
    src.api.club_events
    ~~~~~~~~~~~~~~~~~~~

    Functions:

        update_events()

"""
from flask import Blueprint, request, current_app
from mongoengine.errors import ValidationError
from werkzeug.exceptions import BadRequest, Unauthorized
import dateutil.parser
from src.models.club_event import ClubEvent

club_events_blueprint = Blueprint("club_events", __name__)


@club_events_blueprint.route("/club/update_events/", methods=["PUT"])
def update_events():
    """
    Updates the Club Events.
    ---
    tags:
        - club
    security:
        - ApiKeyAuth: []
    summary: Update Club Events
    requestBody:
        content:
            application/json:
                schema:
                    type: array
                    items:
                        $ref: '#/components/schemas/ClubEvent'
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        401:
            description: Invalid or Missing API Key.
        5XX:
            description: Unexpected error.
    """
    data = request.get_json()

    if not data:
        raise BadRequest()

    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise Unauthorized()

    if auth_token != current_app.config["CLUBEVENT_APIKEY"]:
        raise Unauthorized()

    ClubEvent.drop_collection()

    for event in data:

        if event["date"]:
            event["date"] = dateutil.parser.parse(event["date"])

        try:
            ClubEvent.createOne(**event)
        except ValidationError:
            raise BadRequest()

    res = {
        "status": "success",
        "message": "Events successfully updated!"
    }

    return res, 201


@club_events_blueprint.route("/club/get_events/", methods=["GET"])
def get_events():
    """
    Gets the Club Events.
    ---
    tags:
        - club
    summary: Get Club Events
    parameters:
        - in: query
          name: count
          schema:
            type: integer
          description: The number of most recent events to get.
    responses:
        200:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            count:
                                type: integer
                            events:
                                type: array
                                items:
                                    $ref: '#/components/schemas/ClubEvent'
        5XX:
            description: Unexpected error.
    """
    count = request.args.get("count")

    events = ClubEvent.objects.exclude("id")
    if count:
        events = events[:int(count)]

    res = {
        "count": count,
        "events": events
    }

    return res, 200
