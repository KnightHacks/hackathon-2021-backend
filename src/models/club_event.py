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


class Presenter(db.EmbeddedDocument):
    name = db.StringField()
    image = db.ImageField(
        size=(500, 500),
        thumbnail_size=(20, 20)
    )


class ClubEvent(BaseDocument):
    name = db.StringField(required=True)
    image = db.ImageField(
        size=(500, 500),
        thumbnail_size=(20, 20)
    )
    tags = db.ListField(db.StringField())
    presenter = db.EmbeddedDocumentField(Presenter)
    start = db.DateTimeField(requried=True)
    end = db.DateTimeField(requried=True)
    description = db.StringField()
    location = db.StringField()

    meta = {
        "ordering": ["start"]
    }
