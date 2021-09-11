# -*- coding: utf-8 -*-
"""
    src.models.user
    ~~~~~~~~~~~~~~~
    Model definition for Users

    Classes:

        User


"""
from src.common.jwt import encode_jwt, decode_jwt
from flask import current_app as app
from datetime import datetime, timedelta
from src import db, bcrypt
from src.models import BaseDocument
from mongoengine import signals


class User(BaseDocument):

    username = db.StringField(unique=True, required=True)
    password = db.BinaryField(required=True)

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

    def __init__(self, *args, **kwargs):
        conf = app.config["BCRYPT_LOG_ROUNDS"]
        if (kwargs.get("password") is not None
                and isinstance(kwargs.get("password"), str)):
            kwargs["password"] = bcrypt.generate_password_hash(
                kwargs["password"],
                conf)

        super(User, self).__init__(*args, **kwargs)


signals.pre_delete.connect(User.pre_delete, sender=User)
