# -*- coding: utf-8 -*-
"""
    src.common.init_defaults
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Functions:
        init_default_users()

"""
from src.models.user import User


def init_default_users():
    """Initializes the default users"""
    from flask import current_app as app
    with app.app_context():
        notion_uname = app.config.get("NOTION_CRONJOB_USERNAME")
        notion_passwd = app.config.get("NOTION_CRONJOB_PASSWORD")

        if notion_uname and notion_passwd:
            try:
                User.createOne(
                    username=notion_uname,
                    password=notion_passwd,
                    email_verification=True,
                )
            except Exception as err:
                app.logger.error("Notion Job User was not created!", err)
            else:
                app.logger.info("Created Notion Job User Successfully!")
