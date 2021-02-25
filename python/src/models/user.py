# -*- coding: utf-8 -*-
"""
    src.models.user
    ~~~~~~~~~~~~~~~
    Model definition for Users

    Classes:

        User

    Variables:

        ROLES

"""
import jwt
from flask import current_app
from datetime import datetime, timedelta
from src import db
from src.models import BaseDocument
from werkzeug.exceptions import Unauthorized


ROLES = ("HACKER", "EVENTORG", "SPONSOR", "MOD", "ADMIN")


class User(BaseDocument):
    meta = {"allow_inheritance": True}

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    roles = db.ListField(db.StringField(choices=ROLES), required=True)
    email_registration = db.BooleanField(default=False)

    def encode_email_token(self) -> str:
        """Encode the email token"""
        payload = {
            "exp": datetime.utcnow() + timedelta(
                days=current_app.config["TOKEN_EMAIL_EXPIRATION_DAYS"],
                seconds=current_app.config["TOKEN_EMAIL_EXPIRATION_SECONDS"]),
            "iat": datetime.utcnow(),
            "sub": self.username
        }
        return jwt.encode(
            payload,
            current_app.config.get("SECRET_KEY"),
            algorithm="HS256"
        )

    @staticmethod
    def decode_email_token(email_token: str) -> str:
        """Decodes the email token"""
        try:
            payload = jwt.decode(email_token,
                                 current_app.config.get("SECRET_KEY"))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise Unauthorized()
        except jwt.InvalidTokenError:
            raise Unauthorized()
