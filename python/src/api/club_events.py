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
from datetime import datetime, timedelta
from src.models.club_event import ClubEvent
from flask.json import JSONEncoder
from bson import json_util
from src.models import BaseDocument
from mongoengine.queryset import QuerySet


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

        if event.get("date"):
            event["date"] = dateutil.parser.parse(event["date"])
        else:
            event["date"] = None

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
          minimum: 1
          required: false
          description: The number of events to get.
        - in: query
          name: rdate
          required: false
          schema:
            type: string
            enum:
                - Today
                - LastWeek
                - LastMonth
                - LastYear
          description: >
            A relative date range for the events.
            For an exact range, use `start_date` and `end_date` instead.
            `confirmed` must be true or undefined.
        - in: query
          name: start_date
          required: false
          schema:
            type: string
            format: date
          description: >
            The start date for the events. Must be used with `end_date`.
            This parameter is incompatible with `rdate`.
            `confirmed` must be true or undefined.
        - in: query
          name: end_date
          required: false
          schema:
            type: string
            format: date
          description: >
            The end date for the events. Must be used with `start_date`.
            This parameter is incompatible with `rdate`.
            `confirmed` must be true or undefined.
        - in: query
          name: confirmed
          required: false
          schema:
            type: boolean
            default: true
            required: false
            description: If true, the endpoint returns only confirmed events.
    responses:
        200:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            count:
                                type: integer
                                description: >
                                  Total number of ClubEvents that
                                  match the given parameters.
                            events:
                                type: array
                                items:
                                    $ref: '#/components/schemas/ClubEvent'
        5XX:
            description: Unexpected error.
    """
    args = request.args
    query = {}

    if args.get("rdate") and (
            args.get("start_date") or args.get("end_date")):
        raise BadRequest("Parameter `rdate` is incompatible with `start_date` and `end_date`!")  # noqa: E501

    if args.get("confirmed", "true") != "true" and (
            args.get("start_date") or args.get("end_date")
            or args.get("rdate")):
        raise BadRequest("Parameter `confirmed` must be true or undefined while using date parameters!")  # noqa: E501

    if args.get("confirmed", "true") == "true":
        query["date__type"] = "date"

    if args.get("rdate"):
        if args.get("rdate") == "Today":
            pass

    if args.get("start_date") and args.get("end_date"):
        pass

    events = ClubEvent.objects(**query).exclude("id")

    count = args.get("count")
    if count:
        events = events[:int(count)]


    res = {
        "count": events.count(),
        "events": events
    }

    return res, 200
