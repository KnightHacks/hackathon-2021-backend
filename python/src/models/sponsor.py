# -*- coding: utf-8 -*-
"""
    src.models.sponsor
    ~~~~~~~~~~~~~~~
    Model definition for Sponsors

    Classes:

        Sponsor
"""


from src import db
from src.models.user import User


class Sponsor(User):
    sponsor_name = db.StringField()
    logo = db.URLField()
    subscription_tier = db.StringField()

    @property
    def events(self):
        """Gets the Events for this sponsor"""
        from src.models.event import Event

        events = Event.objects(sponsors=self)

        return events

    def to_mongo(self, *args, **kwargs):
        data = super().to_mongo(*args, **kwargs)

        data["events"] = [e for e in self.events]

        return data
