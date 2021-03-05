# -*- coding: utf-8 -*-
"""
    src.config
    ~~~~~~~~~~
    Defines the Configuration Classes for Flask

    Classes:

        BaseConfig
        DevelopmentConfig
        TestingConfig
        ProductionConfig

"""
import os
import logging


class BaseConfig:
    """Base Configuration"""
    DEBUG = False
    TESTING = False
    LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOGGING_LOCATION = "flask-base.log"
    LOGGING_LEVEL = logging.DEBUG
    MONGODB_HOST = os.getenv("MONGO_URI", "mongodb://localhost:27017/test")
    SWAGGER = {
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json"
            }
        ]
    }
    CLUBEVENT_APIKEY = os.getenv("CLUBEVENT_APIKEY")
    TOKEN_EMAIL_EXPIRATION_DAYS = 1
    TOKEN_EMAIL_EXPIRATION_SECONDS = 0
    SECRET_KEY = os.getenv("SECRET_KEY")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://knighthacks.org/")
    BCRYPT_LOG_ROUNDS = 13


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True
    CLUBEVENT_APIKEY = os.getenv("CLUBEVENT_APIKEY", "dev")
    BCRYPT_LOG_ROUNDS = 4
    MAIL_SUPPRESS_SEND = False


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    CLUBEVENT_APIKEY = "testing"
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = "pluto is a planet"
    MAIL_SUPPRESS_SEND = False


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
