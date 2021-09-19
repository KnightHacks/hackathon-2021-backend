# -*- coding: utf-8 -*-
"""
    src.models.hacker
    ~~~~~~~~~~~~~~~~~
    Model Definition for Hackers

    Classes:

        HackerProfile
        Hacker

"""
from flask import current_app as app
from src import db, bcrypt
from src.models import BaseDocument
from src.common.jwt import encode_jwt, decode_jwt
from datetime import datetime, timedelta


class Education_Info(db.EmbeddedDocument):
    college = db.StringField()
    major = db.StringField()
    graduation_date = db.StringField()


class Socials(db.EmbeddedDocument):
    github = db.StringField()
    linkedin = db.StringField()


class Hacker(BaseDocument):  # Stored in the "user" collection

    private_fields = [
        "id",
        "email_verification",
        "email_token_hash"
    ]

    first_name = db.StringField()
    last_name = db.StringField()
    phone_number = db.StringField()
    isaccepted = db.BooleanField(default=False)
    can_share_info = db.BooleanField(default=False)
    rsvp_status = db.BooleanField(default=False)
    beginner = db.BooleanField(default=False)
    ethnicity = db.StringField()
    pronouns = db.StringField()
    edu_info = db.EmbeddedDocumentField(Education_Info)
    resume = db.FileField()
    socials = db.EmbeddedDocumentField(Socials)
    why_attend = db.StringField(max_length=200)
    what_learn = db.ListField()
    in_person = db.BooleanField(default=False)
    dietary_restrictions = db.StringField()

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
            sub=self.email
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
