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

from flask import Blueprint, request, jsonify
from mongoengine.error import ValidationError
from werkzeug.exceptions import BadRequest, Unauthorized
from src.models.event import Event
from flask_mongoengine import MongoEngine
import dateutil.parser
import json

events_blueprint = Blueprint("events", __name__)

EVENT_FIELDS = ("name", "date", "image", "link", 
                "endDate", "attendeesCount", 
                "eventStatus", "sponsors")


@events_blueprint.route("/events/create_event/", methods=["POST"])
def create_event():
    """
    Creates a new event.
    ---
    tags:
        - hacker
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

    if data["datetime_of_event"]:
        data["datetime_of_event"] = dateutil.parser.parse(data["datetime_of_event"])

    if data["date_when_event_added"]:
        data["date_when_event_added"] = dateutil.parser.parse(data["date_when_event_added"])

    data["event"] = {}

    for field in EVENT_FIELDS:
        data["event"][field] = data.pop(field, None)

    try:
        Event.createOne(**data)
    except ValidationError:
        raise BadRequest()
    
    res = {
		"status": "Success",
		"message": "Event was created!"
	}

    return res, 201


@events_blueprint.route("/events/update_event/", methods=["PUT"])
def update_event():
    """
    Updates an event that has already been created.
    ---
    tags:
        - hacker
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
    # get data
    data = request.get_json()

    if not data:
        raise BadRequest()

    # create a temp object to hold new data
    updated_event = Event.objects(name = data['name'], 
                                  date = data['date'], 
                                  image = data['image'], 
                                  link = data['link'], 
                                  endDate = data['endDate'], 
                                  attendeesCount = data['attendeesCount'], 
                                  eventStatus = data['eventStatus'], 
                                  sponsors = data['sponsors'])
    updated_event.save()

    res = {
        "status": "success",
        "message": "Event was updated!"
    }
    
    return res, 201
    