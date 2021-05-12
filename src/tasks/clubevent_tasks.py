# -*- coding: utf-8 -*-
"""
    src.tasks.mail_tasks
    ~~~~~~~~~~~~~~~~~~~~

    Functions:

        refresh_notion_clubevents()

"""
from src import celery
from src.models.club_event import ClubEvent
from mongoengine.errors import ValidationError
from datetime import datetime


@celery.task
def refresh_notion_clubevents():
    from flask import current_app as app
    with app.app_context():
        ClubEvent.drop_collection()

        # TODO: Use the Notion API when it is released.

        try:
            ClubEvent.objects.insert([
                ClubEvent(name="example", date=datetime.now())
            ])
        except ValidationError:
            app.logger.warning(
                "Invalid Club Events from Notion, did not refresh!"
            )
