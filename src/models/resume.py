# -*- coding: utf-8 -*-
"""
    src.models.resume
    ~~~~~~~~~~~~~~~~~

"""
from src import db
from src.models import BaseDocument
from datetime import datetime


class Resume(BaseDocument):
    file = db.FileField(required=True)
    attached = db.BooleanField(default=False)
    created = db.DateTimeField(default=datetime.utcnow)
    meta = {
        "indexes": [
            {
                "fields": ["created"],
                "expireAfterSeconds": 86400,  # Expires after 24 hours
                "partialFilterExpression": {
                    "attached": False
                }
            }
        ]
    }
