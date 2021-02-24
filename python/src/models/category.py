# -*- coding: utf-8 -*-
"""
    src.models.category
    ~~~~~~~~~~~~~~~~~~~
    Model definition for Categories

    Classes:

        Category

"""
from src import db
from src.models import BaseDocument
from src.models.sponsor import Sponsor


class Category(BaseDocument):
    name = db.StringField(unique=True, required=True)
    sponsor = db.ReferenceField(Sponsor)
    description = db.StringField()
