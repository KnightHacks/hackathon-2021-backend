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
from flask import (
    g,
    Flask,
    json,
    before_render_template,
    template_rendered
)  # noqa: E402
from werkzeug.exceptions import HTTPException  # noqa: E402
from flasgger import Swagger  # noqa: E402
from flask_cors import CORS  # noqa: E402
from flask_mongoengine import MongoEngine  # noqa: E402
from flask_mail import Mail  # noqa: E402
from flask_bcrypt import Bcrypt  # noqa: E402
import sentry_sdk  # noqa: E402
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: E402
from sentry_sdk.integrations.celery import CeleryIntegration  # noqa: E402
from flask_socketio import SocketIO  # noqa: E402
from src.tasks import make_celery  # noqa: E402
import yaml  # noqa: E402
import blinker  # noqa

""" Version Number (DO NOT TOUCH) """
__version__ = "2.1.7"


"""Init Extensions"""
db = MongoEngine()
mail = Mail()
bcrypt = Bcrypt()
socketio = SocketIO()


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
            "name": "Knight Hacks Backend Team",
            "email": "development+backend@knighthacks.org",
            "url": "https://github.com/KnightHacks/hackathon-2021-backend/issues"  # noqa: E501
        },
        "version": __version__,
        "license": {
            "name": "MIT License",
            "url": "https://github.com/KnightHacks/hackathon-2021-backend/blob/main/LICENSE.md"  # noqa: E501
        }
    },
    "servers": [
        {
            "url": "https://api.knighthacks.org",
            "description": "Production server"
        },
        {
            "url": "https://stagingapi.knighthacks.org",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:5000",
            "description": "Local Development server"
        }
    ],
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
    app = Flask(__name__,
                static_url_path="/static",
                static_folder=path.join(
                    path.abspath(path.dirname(__file__)), "static"))

    """Flask Config"""
    app_settings = getenv("APP_SETTINGS", "src.config.ProductionConfig")
    app.config.from_object(app_settings)

    if (app_settings == "src.config.ProductionConfig"
            and not app.config.get("SEND_MAIL")):
        app.logger.warning("Sending Emails disabled on production!")

    """Set FLASK_ENV and FLASK_DEBUG cause that doesn't happen auto anymore"""
    if app.config.get("DEBUG"):
        environ["FLASK_ENV"] = "development"  # pragma: nocover
        environ["FLASK_DEBUG"] = "1"  # pragma: nocover

    if app.config.get("SENTRY_DSN"):
        """Initialize Sentry if we're in production"""
        sentry_sdk.init(
            dsn=app.config.get("SENTRY_DSN"),
            environment=app.config.get("SENTRY_ENV"),
            release=f"backend@{__version__}",
            integrations=[FlaskIntegration(), CeleryIntegration()],
            traces_sample_rate=1.0,
            debug=True
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

    from src.common.json import JSONEncoderBase
    app.json_encoder = JSONEncoderBase

    """Register Blueprints"""
    from src.api.auth import auth_blueprint
    from src.api.hackers import hackers_blueprint
    from src.api.sponsors import sponsors_blueprint
    from src.api.stats import stats_blueprint
    from src.api.events import events_blueprint
    from src.api.club_events import club_events_blueprint
    from src.api.email_verification import email_verify_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/api")
    app.register_blueprint(hackers_blueprint, url_prefix="/api")
    app.register_blueprint(sponsors_blueprint, url_prefix="/api")
    app.register_blueprint(stats_blueprint, url_prefix="/api")
    app.register_blueprint(events_blueprint, url_prefix="/api")
    app.register_blueprint(club_events_blueprint, url_prefix="/api")
    app.register_blueprint(email_verify_blueprint, url_prefix="/api")

    """Register Error Handlers"""
    from src.common import error_handlers

    app.register_error_handler(HTTPException, error_handlers.handle_exception)

    """Initialize Celery"""
    celery = make_celery(app)

    @app.before_first_request
    def _init_app():
        from src.common.init_defaults import init_default_users
        init_default_users()

    @before_render_template.connect_via(app)
    def _sentry_pre_render_template(sender, template, context, **extra):

        parent = sentry_sdk.Hub.current.scope.span
        if parent is not None:
            span = parent.start_child(op="flask.render_template")

            span.set_data("flask.render_template.sender", sender)
            span.set_data("flask.render_template.template", template)
            span.set_data("flask.render_template.context", context)
            span.set_data("flask.render_template.extra", extra)

            g._sentry_span_render_template = span

    @template_rendered.connect_via(app)
    def _sentry_template_rendered(sender, template, context, **extra):
        span = g.pop("_sentry_span_render_template", None)

        if span is not None:
            span.finish()

    return app, celery


app, celery = create_app()
