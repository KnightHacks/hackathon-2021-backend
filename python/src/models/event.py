# -*- coding: utf-8 -*-
"""
    src.api.event
    ~~~~~~~~~~~~~

    Functions:

        create_event()
        update_event()

"""

from src import db
from src.models.sponsor import Sponsor
from src.models.user import User


class Event(db.EmbeddedDocument):
    name = db.StringField()
    date = db.DateTime()
    image = db.URLField
    link = db.URLField()
    endDate = db.DateTime()
    attendeesCount = db.IntField()
    eventStatus = db.StringField()
    sponsors = db.ListField(db.ReferenceField(Sponsor))
    user = db.ReferenceField(User)
