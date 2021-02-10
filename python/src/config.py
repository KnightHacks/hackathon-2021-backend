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
    MONGODB_HOST = os.getenv("MONGO_URI")


class DevelopmentConfig(BaseConfig):
    """Development Configuration"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """Testing Configuration"""
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    """Production Configuration"""
    DEBUG = False
