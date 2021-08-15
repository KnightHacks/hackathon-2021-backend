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

class User(BaseDocument):
    meta = {"allow_inheritance": True,
            "ordering": ["date"]}

    email = db.EmailField(unique=True, required=True)
    date = db.DateTimeField(default=datetime.utcnow)
    email_verification = db.BooleanField(default=False)
    email_token_hash = db.BinaryField()

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

signals.pre_delete.connect(User.pre_delete, sender=User)
