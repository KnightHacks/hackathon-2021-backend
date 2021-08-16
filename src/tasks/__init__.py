# -*- coding: utf-8 -*-
"""
    src.tasks
    ~~~~~~~~~
    Setup Celery

    Functions:

        make_celery(app)

"""
from celery import Celery
from celery.signals import worker_process_init
import sentry_sdk
from sentry_sdk.integrations.celery import FlaskIntegration
from sentry_sdk.integrations.celery import CeleryIntegration


def make_celery(app) -> Celery:
    """Initialize the Celery Application"""

    celery = Celery(
        app.import_name,
        backend=app.config["RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["src.tasks.mail_tasks", "src.tasks.clubevent_tasks"],
        worker_send_task_events=True,
        task_send_sent_event=True
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    @worker_process_init.connect
    def init_sentry(*args, **kwargs):
        if app.config.get("SENTRY_DSN"):
            sentry_sdk.init(
                dsn=app.config.get("SENTRY_DSN"),
                integrations=[
                    FlaskIntegration(),
                    CeleryIntegration()
                ],
                traces_sample_rate=1.0
            )

    return celery
