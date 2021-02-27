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
from enum import IntFlag, auto


class ROLES(IntFlag):
    HACKER = auto()
    EVENTORG = auto()
    SPONSOR = auto()
    MOD = auto()
    ADMIN = auto()


class User(BaseDocument):
    meta = {"allow_inheritance": True}

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    roles = db.EnumField(enum=ROLES, required=True)
