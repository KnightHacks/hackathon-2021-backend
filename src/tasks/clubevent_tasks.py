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
from io import BytesIO
# from PIL import Image


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

            presenterImage = p["Presenter Image"]["files"]
            presenterImage = ("" if not presenterImage
                              else presenterImage[0]["file"]["url"])
            eventImage = p["Image"]["files"]
            eventImage = ("" if not eventImage
                          else eventImage[0]["file"]["url"])

            return {
                "name": p["Name"]["title"][0]["plain_text"],
                "tags": tuple(
                    map(lambda t: t["name"], p["Tags"]["multi_select"])
                ),
                "presenter": {
                    "name": p["Presenter"]["rich_text"][0]["plain_text"],
                    "image": presenterImage
                },
                "start": start_date,
                "end": end_date,
                "description": p["Description"]["rich_text"][0]["plain_text"],
                "location": p["Location"]["rich_text"][0]["plain_text"],
                "image": eventImage
            }

        ClubEvent.drop_collection()

        res = requests.post(
            app.config.get("NOTION_API_URI")
            + f"/databases/{app.config.get('NOTION_DB_ID')}/query",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {app.config.get('NOTION_TOKEN')}",
                "Notion-Version": app.config.get("NOTION_VERSION")
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
                if event["image"]:
                    image = requests.get(event["image"], allow_redirects=True)
                else:
                    image = None
                if event["presenter"]["image"]:
                    presenter_image = requests.get(event["presenter"]["image"],
                                                   allow_redirects=True)
                else:
                    presenter_image = None

                del event["image"]
                del event["presenter"]["image"]

                ce = ClubEvent(**event)

                if image is not None:
                    ce.image.put(
                        BytesIO(image.content),
                        content_type=image.headers.get("content-type")
                    )

                if presenter_image is not None:
                    p_img_type = presenter_image.headers.get("content-type")
                    ce.presenter.image.put(
                        BytesIO(presenter_image.content),
                        content_type=p_img_type
                    )

                ce.save()

            except ValidationError as err:
                app.logger.warning(
                    "Invalid Club Event(s) from Notion, did not refresh!"
                )
                app.logger.info(err)
            else:
                app.logger.info(
                    "Club Event(s) grabbed from Notion, refresh successfull!"
                )
