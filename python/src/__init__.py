import os

from flask import Config, Flask
from flasgger import Swagger
from flask_cors import CORS
from flask_mongoengine import MongoEngine

import yaml

# Flask Config
conf = Config(root_path=os.path.dirname(os.path.realpath(__file__)))
conf.from_object(os.getenv("APP_SETTINGS", "src.config.ProductionConfig"))

# Init Extensions
db = MongoEngine()

# Load the Schema Definitions
schemapath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "schemas.yml")
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
        "schemas": schema
    }
}
swagger = Swagger(template=swagger_template)


def create_app():
    """Initialize the App"""
    app = Flask(__name__, static_url_path="/static")

    # Setup Extensions
    CORS(app)
    db.init_app(app)
    swagger.init_app(app)

    # Register Blueprints
    from src.api.hackers import hackers_blueprint

    app.register_blueprint(hackers_blueprint, url_prefix="/api/hackers")


    return app

app = create_app()

