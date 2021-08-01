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
from src.common.jwt import encode_jwt, decode_jwt
from flask import current_app as app
from datetime import datetime, timedelta
from src import db, bcrypt
from src.models import BaseDocument
from enum import Flag, auto
from mongoengine import signals


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

    private_fields = [
        "id",
        "password",
        "email_verification",
        "email_token_hash"
    ]

    username = db.StringField(unique=True, required=True)
    email = db.EmailField(unique=True, required=True)
    password = db.BinaryField(required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    roles = db.EnumField(enum=ROLES, required=True)
    email_verification = db.BooleanField(default=False)
    email_token_hash = db.BinaryField()

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        from src.models.tokenblacklist import TokenBlacklist
        TokenBlacklist.objects(user=document).delete()
        app.logger.info("Deleted all tokens from tokenblacklist for "
                        f"the deleted user {document.username}.")

    def encode_auth_token(self) -> str:
        """Encode the auth token"""

        return encode_jwt(
            exp=(
                datetime.utcnow() + timedelta(
                    minutes=app.config["TOKEN_EXPIRATION_MINUTES"],
                    seconds=app.config["TOKEN_EXPIRATION_SECONDS"]
                )
            ),
            sub=self.username
        )

    @staticmethod
    def decode_auth_token(auth_token: str) -> str:
        """Decode the auth token"""
        return decode_jwt(auth_token)["sub"]

    def encode_email_token(self) -> str:
        """Encode the email token"""
        email_token = encode_jwt(
            exp=(
                datetime.utcnow() + timedelta(
                    minutes=app.config["TOKEN_EMAIL_EXPIRATION_MINUTES"],
                    seconds=app.config["TOKEN_EMAIL_EXPIRATION_SECONDS"]
                )
            ),
            sub=self.username
        )

        conf = app.config["BCRYPT_LOG_ROUNDS"]
        email_token_hash = bcrypt.generate_password_hash(email_token, conf)

        self.modify(set__email_token_hash=email_token_hash)
        self.save()

        return email_token

    @staticmethod
    def decode_email_token(email_token: str) -> str:
        """Decodes the email token"""
        return decode_jwt(email_token)["sub"]

    def __init__(self, *args, **kwargs):
        conf = app.config["BCRYPT_LOG_ROUNDS"]
        if (kwargs.get("password") is not None
                and isinstance(kwargs.get('password'), str)):
            kwargs['password'] = bcrypt.generate_password_hash(
                kwargs['password'],
                conf)

        super(User, self).__init__(*args, **kwargs)


signals.pre_delete.connect(User.pre_delete, sender=User)
