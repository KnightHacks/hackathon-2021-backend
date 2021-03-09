# -*- coding: utf-8 -*-
"""
    src.tasks.mail_tasks
    ~~~~~~~~~~~~~~~~~~~~

    Functions:

        send_async_email()

"""
from flask import current_app
from flask_mail import Message
from src import celery, mail


@celery.task
def send_async_email(subject, recipient, text_body, html_body):
    """Sends an Email"""
    msg = Message(subject=subject, recipients=[recipient])
    msg.body = text_body
    msg.html = html_body
    if not current_app.config.get("SUPRESS_EMAIL"):
        mail.send(msg)  # pragma: no cover
