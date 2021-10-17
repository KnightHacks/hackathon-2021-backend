# -*- coding: utf-8 -*-
"""
    src.common.mail
    ~~~~~~~~~~~~~~~

"""
from flask import render_template, current_app as currapp
from src.tasks.mail_tasks import send_async_email


def send_verification_email(hacker):
    """Sends a verification email to the user"""

    token = hacker.encode_email_token()

    if not currapp.config["SEND_MAIL"]:
        return
    href = (f"{currapp.config['BACKEND_URL']}api/email/verify?token={token}"
            f"&redirect_uri={currapp.config['FRONTEND_URL']}")
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="Knight Hacks - Verify your Email",
            recipient=hacker.email,
            text_body=render_template("emails/email_verification.txt",
                                      hacker=hacker),
            html_body=render_template("emails/email_verification.html",
                                      hacker=hacker, href=href)))


def send_hacker_acceptance_email(hacker):
    """Sends an acceptance email to the hacker"""
    if not currapp.config["SEND_MAIL"]:
        return
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="Knight Hacks - You're in!",
            recipient=hacker.email,
            text_body=render_template("emails/hacker_acceptance.txt",
                                      hacker=hacker),
            html_body=render_template(
                "emails/hacker_acceptance.html",
                hacker=hacker,
                deadline=currapp.config["HACKER_CONFIRM_DEADLINE"])))


def send_hacker_confirmation_success_email(hacker):
    """Sends an confirmation success email to the hacker"""
    if not currapp.config["SEND_MAIL"]:
        return
    if not currapp.config.get("TESTING"):
        send_async_email.apply_async((), dict(
            subject="Knight Hacks - Thank you for Confirming!",
            recipient=hacker.email,
            text_body=render_template("emails/hacker_confirmation_success.txt",
                                      hacker=hacker),
            html_body=render_template(
                "emails/hacker_confirmation_success.html",
                hacker=hacker)))
