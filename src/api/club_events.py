# -*- coding: utf-8 -*-
"""
    src.api.club_events
    ~~~~~~~~~~~~~~~~~~~

    Functions:

        update_events()

"""
from flask import request, make_response
from src.api import Blueprint
from werkzeug.exceptions import BadRequest, NotFound
import dateutil.parser
from datetime import datetime, timedelta
from src.models.club_event import ClubEvent
from src.common.decorators import authenticate, requires_scope
import base64
from src.common.scope import Scope


club_events_blueprint = Blueprint("club_events", __name__)


@club_events_blueprint.put("/club/refresh_events/")
@authenticate
@requires_scope(Scope.ClubEvent_Refresh)
def refresh_events():
    """
    Refreshed the Club Events from Notion.
    ---
    tags:
        - club
    summary: Refreshes Club Events
    responses:
        200:
            description: OK
    """

    from src.tasks.clubevent_tasks import refresh_notion_clubevents
    refresh_notion_clubevents.apply_async()

    res = {
        "status": "success",
        "message": "Events successfully refreshed!"
    }

    return res, 201


@club_events_blueprint.get("/club/get_events/")
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
                - NextWeek
                - NextMonth
                - NextYear
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

    if args.get("confirmed", "true") != "true" and (args.get("start_date") or args.get("end_date") or args.get("rdate")):  # noqa: E501
        raise BadRequest("Parameter `confirmed` must be true or undefined while using date parameters!")  # noqa: E501

    if args.get("confirmed", "true") == "true":
        query["start__type"] = "date"

    if args.get("rdate"):
        now = datetime.now()
        now = now.replace(hour=0,
                          minute=0,
                          second=0,
                          microsecond=0)

        if args.get("rdate") == "Today":
            query["start__gte"] = now
        elif args.get("rdate") == "NextWeek":
            query["start__gte"] = now
            query["start__lte"] = now + timedelta(days=7)
        elif args.get("rdate") == "NextMonth":
            query["start__gte"] = now
            query["start__lte"] = now + timedelta(days=30)
        elif args.get("rdate") == "NextYear":
            query["start__gte"] = now
            query["start__lte"] = now + timedelta(days=365)

    if args.get("start_date") and args.get("end_date"):
        query |= {
            "start__gte": dateutil.parser.parse(args["start_date"]),
            "start__lt": dateutil.parser.parse(args["end_date"])
        }

    events = ClubEvent.objects(**query)

    count = args.get("count")
    if count:
        events = events[:int(count)]

    event_array = []
    for e in events:
        if e.image:
            img = e.image.thumbnail.read()
            if img is not None:
                image = (
                    "data:image/png;base64," +
                    base64.b64encode(img).decode("utf-8")
                )
            else:
                image = None
        else:
            image = None
        if e.presenter.image:
            img = e.presenter.image.thumbnail.read()
            if img is not None:
                pres_image = (
                    "data:image/png;base64," +
                    base64.b64encode(img).decode("utf-8")
                )
            else:
                pres_image = None
        else:
            pres_image = None
        newE = e.to_mongo().to_dict()

        newE["image"] = image

        newE["presenter"]["image"] = pres_image

        event_array.append(newE)

    res = {
        "count": events.count(),
        "events": event_array
    }

    return res, 200


@club_events_blueprint.get("/club/<id>/image/")
def get_club_event_image(id):
    """
    Gets the image for the specified Club Event
    ---
    tags:
        - club
    parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
    responses:
        200:
            content:
                image/png:
                    schema:
                        type: string
                        format: binary
                image/*:
                    schema:
                        type: string
                        format: binary
    """
    event = ClubEvent.objects(id=id).first()

    if not event:
        raise NotFound("Club Event with the specified id was not found.")

    img = event.image.read()

    if not img:
        raise NotFound("Specified Club Event does not have an image.")

    res = make_response(img)
    res.headers["Content-Type"] = event.image.content_type

    return res


@club_events_blueprint.get("/club/<id>/presenter/image/")
def get_club_event_presenter_image(id):
    """
    Gets the presenter image for the specified Club Event
    ---
    tags:
        - club
    parameters:
        - in: path
          name: id
          required: true
          schema:
            type: string
    responses:
        200:
            content:
                image/png:
                    schema:
                        type: string
                        format: binary
                image/*:
                    schema:
                        type: string
                        format: binary
    """
    event = ClubEvent.objects(id=id).first()

    if not event:
        raise NotFound("Club Event with the specified id was not found.")

    img = event.presenter.image.read()

    if not img:
        raise NotFound("Specified Club Event does not have an image.")

    res = make_response(img)
    res.headers["Content-Type"] = event.presenter.image.content_type

    return res
