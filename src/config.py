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
    TOKEN_EMAIL_EXPIRATION_MINUTES = 30
    TOKEN_EMAIL_EXPIRATION_SECONDS = 0
    SECRET_KEY = os.environ.get("SECRET_KEY", 'pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw')
    RABBITMQ_URL = os.getenv("RABBITMQ_URL")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", RABBITMQ_URL)
    SOCKETIO_MESSAGE_QUEUE = os.getenv("SOCKETIO_MESSAGE_QUEUE", RABBITMQ_URL)
    RESULT_BACKEND = os.getenv("RESULT_BACKEND")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://knighthacks.org/")
    BACKEND_URL = os.getenv("BACKEND_URL", "https://api.knighthacks.org/")
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_MINUTES = 15
    TOKEN_EXPIRATION_SECONDS = 0
    NOTION_CRONJOB_USERNAME = os.getenv("NOTION_CRONJOB_USERNAME")
    NOTION_CRONJOB_PASSWORD = os.getenv("NOTION_CRONJOB_PASSWORD")
    NOTION_DB_ID = os.getenv("NOTION_DB_ID")
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_API_URI = os.getenv("NOTION_API_URI", "https://api.notion.com/v1")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", '146585145368132386173505678016728509634')


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    MAIL_SUPPRESS_SEND = False
    SUPPRESS_EMAIL = True


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SECRET_KEY = "pluto is a planet"
    TOKEN_EXPIRATION_MINUTES = 1440
    MAIL_SUPPRESS_SEND = False
    SUPPRESS_EMAIL = True


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
    SENTRY_DSN = os.getenv("SENTRY_DSN")
