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
from enum import Flag, auto


class ROLES(Flag):
    HACKER = auto()
    EVENTORG = auto()
    SPONSOR = auto()
    MOD = auto()
    ADMIN = auto()

    @staticmethod
    def members():
        return {r.name: r for r in ROLES}

    @classmethod
    def _missing_(cls, value):
        members = cls.members()
        if value in members.keys():
            return cls(members[value])
        return super()._missing_(value)


class User(BaseDocument):
    meta = {"allow_inheritance": True}

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    roles = db.EnumField(enum=ROLES, required=True)
