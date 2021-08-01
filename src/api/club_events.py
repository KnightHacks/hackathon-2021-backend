# -*- coding: utf-8 -*-
"""
    src.api.club_events
    ~~~~~~~~~~~~~~~~~~~

    Functions:

        update_events()

"""
from flask import request
from src.api import Blueprint
from werkzeug.exceptions import BadRequest
import dateutil.parser
from datetime import datetime, timedelta
from src.models.club_event import ClubEvent
from src.common.decorators import authenticate, privileges
from src.models.user import ROLES


club_events_blueprint = Blueprint("club_events", __name__)


@club_events_blueprint.put("/club/refresh_events/")
@authenticate
@privileges(ROLES.EVENTORG | ROLES.MOD | ROLES.ADMIN)
def refresh_events(_):
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

    events = ClubEvent.objects(**query).exclude("id")

    count = args.get("count")
    if count:
        events = events[:int(count)]

    res = {
        "count": events.count(),
        "events": events
    }

    return res, 200
