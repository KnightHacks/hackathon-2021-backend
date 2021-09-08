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


class Education_Info(db.EmbeddedDocument):
    college = db.StringField()
    major = db.StringField()
    graduation_date = db.IntField()


class Socials(db.EmbeddedDocument):
    github = db.StringField()
    linkedin = db.StringField()


class Hacker(User):  # Stored in the "user" collection
    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    isaccepted = db.BooleanField(default=False)
    can_share_info = db.BooleanField(default=False)
    rsvp_status = db.BooleanField(default=False)
    beginner = db.BooleanField(default=False)
    ethnicity = db.StringField()
    pronouns = db.StringField()
    edu_info = db.EmbeddedDocumentField(Education_Info)
    resume = db.FileField()
    socials = db.EmbeddedDocumentField(Socials)
    why_attend = db.StringField(max_length=200)
    what_learn = db.ListField()
    in_person = db.BooleanField(default=False)
