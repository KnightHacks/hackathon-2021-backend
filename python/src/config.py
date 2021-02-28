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


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True
    CLUBEVENT_APIKEY = os.getenv("CLUBEVENT_APIKEY", "dev")


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True
    CLUBEVENT_APIKEY = "testing"


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
