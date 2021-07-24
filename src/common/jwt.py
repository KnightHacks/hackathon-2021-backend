# -*- coding: utf-8 -*-
"""
    src.common.jwt
    ~~~~~~~~~~~~~~
    Helper functions for JWT tokens

"""
import jwt
import uuid
from flask import current_app
from werkzeug.exceptions import Unauthorized
from datetime import datetime


def encode_jwt(exp: datetime, sub: str):
    return jwt.encode(
        {
            "exp": exp,
            "iat": datetime.utcnow(),
            "sub": sub,
            "jti": str(uuid.uuid4()),
            "iss": current_app.config.get("BACKEND_URL")
        },
        current_app.config.get("SECRET_KEY"),
        algorithm="HS256"
    )


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            current_app.config.get("SECRET_KEY"),
            options={
                "require": ["exp", "iat", "jti", "sub", "iss"],
                "verify_iss": True
            },
            algorithms=["HS256"],
            issuer=current_app.config.get("BACKEND_URL")
        )
    except jwt.ExpiredSignatureError:
        raise Unauthorized()
    except jwt.InvalidTokenError:
        raise Unauthorized()
