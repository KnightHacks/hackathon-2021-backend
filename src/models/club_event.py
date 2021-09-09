# -*- codng: utf-8 -*-
"""
    src.models.club_event
    ~~~~~~~~~~~~~~~~~~~~~
    Model definition for Club Events

    Classes:

        ClubEvent

"""
from src import db
from src.models import BaseDocument


class ClubEvent(BaseDocument):
    name = db.StringField(required=True)
    tags = db.ListField(db.StringField())
    presenter = db.StringField()
    start = db.DateTimeField(requried=True)
    end = db.DateTimeField(requried=True)
    description = db.StringField()
    location = db.StringField()

    meta = {
        "ordering": ["start"]
    }
