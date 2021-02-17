# -*- coding: utf-8 -*-
"""
    src.models.sponsor
    ~~~~~~~~~~~~~~~
    Model definition for Sponsors

    Classes:

        Sponsor
"""
from src import db

class Sponsor():
    sponsor_name = db.StringField()
    logo = db.URLField()
    event_hosting = db.EmbeddedDocument()
    subscription_tier = db.StringField()
