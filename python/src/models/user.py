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
from src import db, bcrypt
from src.models import BaseDocument
from werkzeug.exceptions import Unauthorized
from enum import Flag, auto


class ROLES(Flag):
    HACKER = auto()
    EVENTORG = auto()
    SPONSOR = auto()
    MOD = auto()
    ADMIN = auto()

    @staticmethod
    def members():
        return {r.name: r for r in ROLES}

    @classmethod
    def _missing_(cls, value):
        members = cls.members()
        if value in members.keys():
            return cls(members[value])
        return super()._missing_(value)


class User(BaseDocument):
    meta = {"allow_inheritance": True,
            "ordering": ["date"]}

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    roles = db.ListField(db.StringField(choices=ROLES), required=True)
    email_verification = db.BooleanField(default=False)
    email_token_hash = db.BinaryField()

    def encode_email_token(self) -> str:
        """Encode the email token"""
        payload = {
            "exp": datetime.now() + timedelta(
                days=current_app.config["TOKEN_EMAIL_EXPIRATION_DAYS"],
                seconds=current_app.config["TOKEN_EMAIL_EXPIRATION_SECONDS"]),
            "iat": datetime.now(),
            "sub": self.username
        }
        email_token = jwt.encode(
            payload,
            current_app.config.get("SECRET_KEY"),
            algorithm="HS256"
        )

        conf = current_app.config["BCRYPT_LOG_ROUNDS"]
        email_token_hash = bcrypt.generate_password_hash(email_token, conf)

        self.modify(set__email_token_hash=email_token_hash)
        self.save()

        return email_token

    @staticmethod
    def decode_email_token(email_token: str) -> str:
        """Decodes the email token"""
        try:
            payload = jwt.decode(email_token,
                                 current_app.config.get("SECRET_KEY"),
                                 algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise Unauthorized()
        except jwt.InvalidTokenError:
            raise Unauthorized()
