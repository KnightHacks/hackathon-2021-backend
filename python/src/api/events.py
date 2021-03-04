# -*- coding: utf-8 -*
"""
    src.api.events
    ~~~~~~~~~~~~~~

    Functions:

        create_event()
        update_event()

    Variables:

        EVENT_FIELDS
"""

from flask import Blueprint, request
from mongoengine.errors import ValidationError
from werkzeug.exceptions import BadRequest, NotFound
from src.models.event import Event
from src.models.sponsor import Sponsor
import dateutil.parser

events_blueprint = Blueprint("events", __name__)

EVENT_FIELDS = ("name", "date_time", "description",
                "image", "link", "end_date_time",
                "attendees_count", "event_status",
                "sponsors", "user")


@events_blueprint.route("/events/create_event/", methods=["POST"])
def create_event():
    """
    Creates a new event.
    ---
    tags:
        - event
    summary: Create event
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Event'
        description: Created event object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        5XX:
            description: Unexpected error (the API issue).
    """
    data = request.get_json()

    if not data:
        raise BadRequest()

    if data["date_time"]:
        data["date_time"] = dateutil.parser.parse(data["date_time"])

    if data["end_date_time"]:
        data["end_date_time"] = dateutil.parser.parse(data["end_date_time"])

    if data.get("sponsors"):
        data["sponsors"] = list(
                                map(lambda name: Sponsor.objects(username=name).first(),data["sponsors"]))
    new_data = {}

    for field in EVENT_FIELDS:
        new_data[field] = data.pop(field, None)

    try:
        Event.createOne(**new_data)
    except ValidationError:
        raise BadRequest()

    res = {
        "status": "success",
        "message": "Event was updated!"
    }

    return res, 201


@events_blueprint.route("/events/update_event/", methods=["PUT"])
def update_event():
    """
    Updates an event that has already been created.
    ---
    tags:
        - event
    summary: Updates event
    requestBody:
        content:
            application/json:
                schema:
                    $ref: '#/components/schemas/Event'
        description: Updated event object
        required: true
    responses:
        201:
            description: OK
        400:
            description: Bad request.
        5XX:
            description: Unexpected error (the API issue).
    """
    data = request.get_json()

    if not data:
        raise BadRequest()

    if data["date_time"]:
        data["date_time"] = dateutil.parser.parse(data["date_time"])

    if data["end_date_time"]:
        data["end_date_time"] = dateutil.parser.parse(data["end_date_time"])

    event = Event.objects(name=data["name"]).first()

    if not event:
        raise NotFound()

    event.modify(**data)

    res = {
        "status": "success",
        "message": "Event was updated!"
    }

    return res, 201
