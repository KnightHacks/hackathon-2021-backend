# -*- coding: utf-8 -*-
"""
    src
    ~~~
    Initialize the Flask App and its extensions + blueprints

    Functions:

        create_app() -> Flask

    Variables:

        schema
        swagger_template
        db
        app

"""
from os import path, getenv
from flask import Flask
from werkzeug.exceptions import HTTPException
from flasgger import Swagger
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import yaml


# Init Extensions
db = MongoEngine()

# Load the Schema Definitions
schemapath = path.join(path.abspath(path.dirname(__file__)), "schemas.yml")
schemastream = open(schemapath, "r")
schema = yaml.load(schemastream, Loader=yaml.FullLoader)
schemastream.close()

swagger_template = {
    "openapi": "3.0.3",
    "swagger": "3.0.3",
    "info": {
        "title": "Knight Hacks Backend API",
        "description": "Backend API for Knight Hacks",
        "contact": {
            "responsibleOrganization": "Knight Hacks",
            "responsibleDeveloper": "Knight Hacks Dev Team",
            "email": "webmaster@knighthacks.org",
            "url": "https://knighthacks.org"
        },
        "version": "0.0.1"
    },
    "basePath": "/api",
    "schemes": [
        "http",
        "https"
    ],
    "components": {
        "schemas": schema,
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization"
            }
        }
    }
}
swagger = Swagger(template=swagger_template)


def create_app():
    """Initialize the App"""
    app = Flask(__name__, static_url_path="/static")

    # Flask Config
    app_settings = getenv("APP_SETTINGS", "src.config.ProductionConfig")
    app.config.from_object(app_settings)

    """Setup Extensions"""
    CORS(app)
    db.init_app(app)
    swagger.init_app(app)

    """Register Blueprints"""
    from src.api.hackers import hackers_blueprint
    from src.api.stats import stats_blueprint
    from src.api.sponsor import sponsors_blueprint
    from src.api.events import events_blueprint
    from src.api.groups import groups_blueprint
    from src.api.club_events import club_events_blueprint
    from src.api.categories import categories_blueprint
    from src.api.email_registration import email_reg_blueprint

    app.register_blueprint(hackers_blueprint, url_prefix="/api")
    app.register_blueprint(stats_blueprint, url_prefix="/api")
    app.register_blueprint(sponsors_blueprint, url_prefix="/api")
    app.register_blueprint(events_blueprint, url_prefix="/api")
    app.register_blueprint(groups_blueprint, url_prefix="/api")
    app.register_blueprint(club_events_blueprint, url_prefix="/api")
    app.register_blueprint(categories_blueprint, url_prefix="/api")
    app.register_blueprint(email_reg_blueprint, url_prefix="/api")

    """Register Error Handlers"""
    from src.common import error_handlers

    app.register_error_handler(HTTPException, error_handlers.handle_exception)

    return app


app = create_app()
