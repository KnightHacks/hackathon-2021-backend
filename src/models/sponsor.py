# -*- coding: utf-8 -*-
"""
    src.models.sponsor
    ~~~~~~~~~~~~~~~
    Model definition for Sponsors

    Classes:

        Sponsor
"""
from src.models import BaseDocument
from mongoengine.errors import ValidationError
from src import db


class Sponsor(BaseDocument):
    sponsor_name = db.StringField()
    description = db.StringField()
    logo = db.URLField()
    socials = db.DictField()
    subscription_tier = db.StringField()

    def to_mongo(self, *args, **kwargs):
        data = super().to_mongo(*args, **kwargs)

        try:
            data["events"] = [e for e in self.events]
        except ValidationError:
            pass

        return data
