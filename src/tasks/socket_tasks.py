# -*- coding: utf-8 -*-
"""
    src.tasks.socket_tasks
    ~~~~~~~~~~~~~~~~~~~~

    Functions:

        send_msg_to_client()

"""
from src import celery
from flask_socketio import send, emit
from flask import current_app as app


@celery.task
def broadcast_ws_message(data: dict, namespace: str = None):
    """Broadcasts events to websocket clients"""
    with app.app_context():
        send(data, namespace=namespace, broadcast=True)


@celery.task
def broadcast_ws_event(event: str, data: dict = None, namespace: str = None):
    """Broadcasts events to websocket clients"""
    with app.app_context():
        emit(event, data, namespace=namespace, broadcast=True)
