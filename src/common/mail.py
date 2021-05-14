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
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="Knight Hacks - Verify your Email",
            recipient=user.email,
            text_body=render_template("emails/email_verification.txt",
                                      user=user),
            html_body=render_template("emails/email_verification.html",
                                      user=user, href=href)))


def send_event_email(user, event):
    pass


def send_track_email(user, track):
    pass


def send_hacker_acceptance_email(hacker):
    """Sends an acceptance email to the hacker"""
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="",
            recipient=hacker.email,
            text_body=render_template("emails/hacker_acceptance.txt",
                                      hacker=hacker),
            html_body=render_template("emails/hacker_acceptance.html",
                                      hacker=hacker)))


def send_sponsor_acceptance_email(sponsor):
    """Sends an acceptance email to the sponsor"""
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="",
            recipient=sponsor.email,
            text_body=render_template("emails/sponsor_acceptance.txt",
                                      sponsor=sponsor),
            html_body=render_template(
                "emails/sponsor_acceptance.html",
                sponsor=sponsor)))
