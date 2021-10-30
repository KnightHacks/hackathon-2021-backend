# -*- coding: utf-8 -*
"""
    src.api.events
    ~~~~~~~~~~~~~~
    Functions:
        create_event()
        update_event()
        get_all_events()
    Variables:
        EVENT_FIELDS
"""

from flask import request
from src.api import Blueprint
from mongoengine.errors import NotUniqueError
from werkzeug.exceptions import BadRequest, NotFound, Conflict
from src.models.event import Event
import dateutil.parser
from dateutil.parser import ParserError
from src.common.decorators import authenticate, requires_scope
from src.common.scope import Scope

events_blueprint = Blueprint("events", __name__)

EVENT_FIELDS = ("name", "date_time", "description",
                "image", "link", "end_date_time",
                "attendees_count", "event_status",
                "event_type", "loc")


@events_blueprint.post("/events/create_event/")
@authenticate
@requires_scope(Scope.Event_Create)
def create_event():
    """
    Creates a new event.
    ---
    tags:
        - event
    summary: Creates event
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

    if data.get("date_time"):
        try:
            data["date_time"] = dateutil.parser.parse(data["date_time"])
        except ParserError:
            raise BadRequest()

    if data.get("end_date_time"):
        try:
            data["end_date_time"] = dateutil.parser.parse(data["end_date_time"])  # noqa: E501
        except ParserError:
            raise BadRequest()

    new_data = {}

    for field in EVENT_FIELDS:
        new_data[field] = data.pop(field, None)

    try:
        Event.createOne(**new_data)
    except NotUniqueError:
        raise Conflict("The event name already exists.")

    res = {
        "status": "success",
        "message": "Event was created!"
    }

    return res, 201


@events_blueprint.put("/events/update_event/<event_name>/")
@authenticate
@requires_scope(Scope.Event_Update)
def update_event(event_name: str):
    """
    Updates an event that has already been created.
    ---
    tags:
        - event
    summary: Updates event
    parameters:
        - id: event_name
          in: path
          description: event name
          required: true
          schema:
            type: string
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

    if data.get("date_time"):
        try:
            data["date_time"] = dateutil.parser.parse(data["date_time"])
        except ParserError:
            raise BadRequest()

    if data.get("end_date_time"):
        try:
            data["end_date_time"] = dateutil.parser.parse(data["end_date_time"])  # noqa: E501
        except ParserError:
            raise BadRequest()

    event = Event.objects(name=event_name).first()

    if not event:
        raise NotFound()

    event.modify(**data)

    res = {
        "status": "success",
        "message": "Event was updated!"
    }

    return res, 201


@events_blueprint.get("/events/get_all_events/")
def get_all_events():
    """
    Returns an array of event documents.
    ---
    tags:
        - event
    summary: returns an array of event documents
    responses:
        201:
            description: OK
        5XX:
            description: Unexpected error (the API issue).
    """
    events = Event.objects()

    if not events:
        raise NotFound("There are no events created.")

    res = {
        "events": events,
        "status": "success"
    }

    return res, 201
