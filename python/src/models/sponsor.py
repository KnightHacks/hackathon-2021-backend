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
#from src.models.event import Event


class Sponsor(User):
    sponsor_name = db.StringField()
    logo = db.URLField()
    #event_hosting = db.ListField(db.ReferenceField(Event))
    subscription_tier = db.StringField()
