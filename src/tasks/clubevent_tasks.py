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
import requests
import dateutil.parser
from datetime import datetime, timedelta


@celery.task
def refresh_notion_clubevents():
    from flask import current_app as app
    with app.app_context():

        def clean_notion(r: dict) -> dict:
            p = r["properties"]

            def fix_date(d: str) -> datetime:
                if not d:
                    return None
                return dateutil.parser.parse(d)

            start_date = fix_date(p["Date"]["date"]["start"])
            end_date = fix_date(p["Date"]["date"]["end"])
            if end_date is None:
                end_date = start_date + timedelta(hours=1)

            return {
                "name": p["Name"]["title"][0]["plain_text"],
                "tags": tuple(
                    map(lambda t: t["name"], p["Tags"]["multi_select"])
                ),
                "presenter": p["Presenter"]["rich_text"][0]["plain_text"],
                "start": start_date,
                "end": end_date,
                "description": p["Description"]["rich_text"][0]["plain_text"],
                "location": p["Location"]["rich_text"][0]["plain_text"]
            }

        ClubEvent.drop_collection()

        res = requests.post(
            app.config.get("NOTION_API_URI")
            + f"/databases/{app.config.get('NOTION_DB_ID')}/query",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {app.config.get('NOTION_TOKEN')}",
                "Notion-Version": "2021-07-27"
            },
            json={
                "filter": {
                    "and": [
                        {
                            "property": "Name",
                            "text": {"is_not_empty": True}
                        },
                        {
                            "property": "Tags",
                            "multi_select": {"is_not_empty": True}
                        },
                        {
                            "property": "Presenter",
                            "text": {"is_not_empty": True}
                        },
                        {
                            "property": "Date",
                            "date": {"is_not_empty": True}
                        },
                        {
                            "property": "Location",
                            "text": {"is_not_empty": True}
                        },
                        {
                            "property": "Description",
                            "text": {"is_not_empty": True}
                        }
                    ]
                }
            }
        )

        raw_data = res.json().get("results", [])

        data = map(clean_notion, raw_data)

        for event in data:
            try:
                ClubEvent.createOne(**event)
            except ValidationError:
                app.logger.warning(
                    "Invalid Club Event(s) from Notion, did not refresh!"
                )
            else:
                app.logger.info(
                    "Club Event(s) grabbed from Notion, refresh successfull!"
                )
