# -*- coding: utf-8 -*-
"""
    src.models.group
    ~~~~~~~~~~~~~~~~
    Model definition for Groups

    Classes:

        Group

"""
from datetime import datetime
from src import db
from src.models import BaseDocument
from src.models.hacker import Hacker


class Group(BaseDocument):
    name = db.StringField(unique=True, required=True)
    icon = db.StringField()
    members = db.ListField(db.ReferenceField(Hacker))
    categories = db.ListField(db.StringField())
    date = db.DateTimeField(default=datetime.utcnow)

    @staticmethod
    def member_fields(member: Hacker) -> dict:
        return {
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "username": member.username
        }

    def to_mongo(self, *args, **kwargs):
        data = super().to_mongo(*args, **kwargs)

        data["members"] = [self.member_fields(m) for m in self.members]

        return data
