# -*- coding: utf-8 -*-
"""
    src.models.hacker
    ~~~~~~~~~~~~~~~~~
    Model Definition for Hackers

    Classes:

        HackerProfile
        Hacker

"""
from src import db
from src.models.user import User
from mongoengine import signals


class HackerProfile(db.EmbeddedDocument):
    school_name = db.StringField()
    grad_year = db.IntField()
    resume = db.URLField()
    socials = db.ListField(db.StringField())


class Hacker(User):  # Stored in the "user" collection
    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    tracks = db.ListField(db.StringField())
    current_status = db.BooleanField()
    hacker_profile = db.EmbeddedDocumentField(HackerProfile)
    isaccepted = db.BooleanField(default=False)


signals.pre_delete.connect(User.pre_delete, sender=Hacker)
