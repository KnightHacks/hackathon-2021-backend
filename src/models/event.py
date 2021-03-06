# -*- coding: utf-8 -*-
"""
    src.api.event
    ~~~~~~~~~~~~~
    Model definition for Event

    Classes:

        Event

"""

from src import db
from src.models import BaseDocument


class Event(BaseDocument):
    name = db.StringField(unique=True, required=True)
    date_time = db.DateTimeField(required=True)
    description = db.StringField()
    image = db.URLField()
    link = db.URLField(required=True)
    end_date_time = db.DateTimeField(required=True)
    attendees_count = db.IntField()
    event_status = db.StringField()
    event_type = db.StringField()
    loc = db.StringField()
