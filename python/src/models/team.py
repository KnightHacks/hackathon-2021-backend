# -*- coding: utf-8 -*-
"""
    src.models.team
    ~~~~~~~~~~~~~~~
    Model definition for Teams

    Classes:

        Team

"""
from datetime import datetime
from src import db
from src.models import BaseDocument
from src.models.hacker import Hacker


class Team(BaseDocument):
    name = db.StringField(unique=True, required=True)
    icon = db.StringField()
    members = db.ListField(db.ReferenceField(Hacker))
    categories = db.ListField(db.StringField())
    date = db.DateTimeField(default=datetime.utcnow)
