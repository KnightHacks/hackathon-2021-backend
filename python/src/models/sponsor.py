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
