# -*- coding: utf-8 -*-
"""
    src.models.live_update
    ~~~~~~~~~~~~~~~~~~~~~~
    Model definition for LiveUpdate

    Classes:

        LiveUpdate

"""
from datetime import datetime
from src import db
from src.models import BaseDocument


class LiveUpdate(BaseDocument):
    ID = db.SequenceField(unique=True)
    timestamp = db.DateTimeField(default=datetime.now)
    message = db.StringField(required=True)

    meta = {
        "ordering": ["date"]
    }
