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
from os import path, getenv, environ
if not getenv("APP_SETTINGS", "src.config.TestingConfig"):
    from gevent import monkey
    monkey.patch_all()
from flask import Flask, json  # noqa: E402
from werkzeug.exceptions import HTTPException  # noqa: E402
from flasgger import Swagger  # noqa: E402
from flask_cors import CORS  # noqa: E402
from flask_mongoengine import MongoEngine  # noqa: E402
from flask_mail import Mail  # noqa: E402
from flask_bcrypt import Bcrypt  # noqa: E402
from flask_security import Security, MongoEngineUserDatastore, UserMixin, RoleMixin # noqa: E402
import sentry_sdk  # noqa: E402
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: E402
from sentry_sdk.integrations.celery import CeleryIntegration  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
from src.tasks import make_celery  # noqa: E402
import yaml  # noqa: E402


"""Init Extensions"""
db = MongoEngine()
mail = Mail()
bcrypt = Bcrypt()
socketio = SocketIO()
security = Security()


"""Load the Schema Definitions"""
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
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "sid"
            }
        }
    }
}
swagger = Swagger(template=swagger_template)


def create_app():
    """Initialize the App"""
    app = Flask(__name__, static_url_path="/static")

    """Flask Config"""
    app_settings = getenv("APP_SETTINGS", "src.config.ProductionConfig")
    app.config.from_object(app_settings)

    """Set FLASK_ENV and FLASK_DEBUG cause that doesn't happen auto anymore"""
    if app.config.get("DEBUG"):
        environ["FLASK_ENV"] = "development"  # pragma: nocover
        environ["FLASK_DEBUG"] = "1"  # pragma: nocover
    elif app.config.get("SENTRY_DSN"):
        """Initialize Sentry if we're in production"""
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"),
            integrations=[FlaskIntegration(), CeleryIntegration()],
            traces_sample_rate=1.0
        )

    """Setup Extensions"""
    CORS(app)
    db.init_app(app)
    swagger.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app,
                      cors_allowed_origins="*",
                      json=json,
                      message_queue=app.config.get("SOCKETIO_MESSAGE_QUEUE"))

    from src.models.user import Role, User
    from src.models.hacker import Hacker
    app.user_datastore = MongoEngineUserDatastore(db, User, Role)
    app.hacker_datastore = MongoEngineUserDatastore(db, Hacker, Role)
    security.init_app(app, datastore=app.hacker_datastore)

    from src.common.json import JSONEncoderBase
    app.json_encoder = JSONEncoderBase

    """Register Blueprints"""
    from src.api.hackers import hackers_blueprint
    from src.api.stats import stats_blueprint
    from src.api.sponsor import sponsors_blueprint
    from src.api.events import events_blueprint
    from src.api.groups import groups_blueprint
    from src.api.club_events import club_events_blueprint
    from src.api.categories import categories_blueprint
    from src.api.email_verification import email_verify_blueprint
    from src.api.auth import auth_blueprint
    from src.api.admin import admin_blueprint
    from src.api.live_updates import live_updates_blueprint

    app.register_blueprint(hackers_blueprint, url_prefix="/api")
    app.register_blueprint(stats_blueprint, url_prefix="/api")
    app.register_blueprint(sponsors_blueprint, url_prefix="/api")
    app.register_blueprint(events_blueprint, url_prefix="/api")
    app.register_blueprint(groups_blueprint, url_prefix="/api")
    app.register_blueprint(club_events_blueprint, url_prefix="/api")
    app.register_blueprint(categories_blueprint, url_prefix="/api")
    app.register_blueprint(email_verify_blueprint, url_prefix="/api")
    app.register_blueprint(auth_blueprint, url_prefix="/api")
    app.register_blueprint(admin_blueprint, url_prefix="/api")
    app.register_blueprint(live_updates_blueprint, url_prefix="/api")

    """Register SocketIO Namespaces"""
    from src.api.live_updates import LiveUpdates

    socketio.on_namespace(LiveUpdates("/liveupdates"))

    """Register Error Handlers"""
    from src.common import error_handlers

    app.register_error_handler(HTTPException, error_handlers.handle_exception)

    """Initialize Celery"""
    celery = make_celery(app)

    @app.before_first_request
    def _init_app():
        from src.common.init_defaults import init_default_users
        init_default_users()

        """ Create expiration index for TokenBlacklist """
        from src.models.tokenblacklist import TokenBlacklist
        TokenBlacklist.create_index("created_at", expireAfterSeconds=(
            60 * app.config.get("TOKEN_EXPIRATION_MINUTES")
            + app.config.get("TOKEN_EXPIRATION_SECONDS")
        ), background=True)

    return app, celery


app, celery = create_app()
