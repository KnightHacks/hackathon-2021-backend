# -*- coding: utf-8 -*-
"""
    src.models.user
    ~~~~~~~~~~~~~~~
    Model definition for Users

    Classes:

        User


"""
from flask import current_app as app
from src import db, bcrypt
from datetime import datetime, timedelta
from src.models import BaseDocument
from werkzeug.exceptions import Unauthorized
import jwt


class User(BaseDocument):

    username = db.StringField(unique=True, required=True)
    password = db.BinaryField(required=True)

    def encode_auth_token(self) -> str:
        """Encode the auth token"""
        payload = {
            "exp": datetime.now() + timedelta(
                minutes=app.config["TOKEN_EXPIRATION_MINUTES"],
                seconds=app.config["TOKEN_EXPIRATION_SECONDS"]),
            "iat": datetime.now(),
            "sub": self.username
        }

        return jwt.encode(
            payload,
            app.config.get("SECRET_KEY"),
            algorithm="HS256"
        )

    @staticmethod
    def decode_auth_token(auth_token: str) -> str:
        """Decode the auth token"""
        try:
            payload = jwt.decode(auth_token,
                                 app.config.get("SECRET_KEY"),
                                 algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Expired Token")
        except jwt.InvalidTokenError:
            raise Unauthorized("Invalid Token")

    def __init__(self, *args, **kwargs):
        conf = app.config["BCRYPT_LOG_ROUNDS"]
        if (kwargs.get("password") is not None
                and isinstance(kwargs.get("password"), str)):
            kwargs["password"] = bcrypt.generate_password_hash(
                kwargs["password"],
                conf)

        super(User, self).__init__(*args, **kwargs)
