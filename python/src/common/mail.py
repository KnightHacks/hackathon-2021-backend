# -*- coding: utf-8 -*-
"""
    src.common.mail
    ~~~~~~~~~~~~~~~

"""
from flask import render_template, current_app as currapp
from src.tasks.mail_tasks import send_async_email


def send_verification_email(user, token):
    """Sends a verification email to the user"""
    href = f"{currapp.config['FRONTEND_URL']}/verifyemail?token={token}"
    send_async_email(subject="Knight Hacks - Verify your Email",
                     recipient=user.email,
                     text_body=render_template("emails/email_verification.txt",
                                               user=user),
                     html_body=render_template("emails/email_verification.html",  # noqa: E501
                                               user=user, href=href))


def send_event_email(user, event):
    pass


def send_track_email(user, track):
    pass


def send_acceptance_email(user):
    pass
