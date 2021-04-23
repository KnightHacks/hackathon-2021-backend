# -*- coding: utf-8 -*-
"""
    src.models.team
    ~~~~~~~~~~~~~~~
    Model definition for Teams

    Classes:

        Team

"""
from mongoengine.errors import ValidationError
from datetime import datetime
from src import db
from src.models import BaseDocument
from src.models.hacker import Hacker
from src.models.category import Category


class Team(BaseDocument):
    name = db.StringField(unique=True, required=True)
    icon_name = db.StringField()
    icon = db.ImageField(
        size=(500, 500, True)
    )
    members = db.ListField(
        db.ReferenceField(Hacker, reverse_delete_rule=4),
        max_length=4
    )
    pending_members = db.ListField(
        db.ReferenceField(Hacker, reverse_delete_rule=4),
        max_length=4
    )
    categories = db.ListField(
        db.ReferenceField(Category, reverse_delete_rule=4)
    )
    date = db.DateTimeField(default=datetime.now)
