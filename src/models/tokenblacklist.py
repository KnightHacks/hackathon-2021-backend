# -*- coding: utf-8 -*-
"""
    server.models.tokenblacklist
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
from flask import current_app
from src import db
from src.models import BaseDocument
from datetime import datetime


class TokenBlacklist(BaseDocument):
    jti = db.StringField(max_length=36, required=True, unique=True)
    created_at = db.DateTimeField(required=True, default=datetime.utcnow)
    revoked = db.BooleanField(default=False, required=True)
    from src.models.user import User
    user = db.ReferenceField(User, required=True)

    meta = {
        "indexes": [
            {
                "fields": ["created_at"],
                "expireAfterSeconds": (
                    60 * current_app.config.get("TOKEN_EXPIRATION_MINUTES")
                    + current_app.config.get("TOKEN_EXPIRATION_SECONDS")
                )
            }
        ]
    }
