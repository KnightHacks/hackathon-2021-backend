# -*- coding: utf-8 -*-
"""
    src.models.user
    ~~~~~~~~~~~~~~~
    Model definition for Users

    Classes:

        User

    Variables:

        ROLES

"""
from datetime import datetime

from src import db
from src.models import BaseDocument


ROLES = ("HACKER", "EVENTORG", "SPONSOR", "MOD", "ADMIN")


class User(BaseDocument):
    meta = {"allow_inheritance": True}

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    permissions = db.ListField(db.StringField(choices=ROLES), required=True)
