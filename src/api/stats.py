# -*- coding: utf-8 -*-
"""
    src.api.stats
    ~~~~~~~~~~~~~

    Functions:

        count_users()

"""
from flask import Blueprint
from src.models.user import User
from src.models.hacker import Hacker
from src.models.sponsor import Sponsor


stats_blueprint = Blueprint("stats", __name__)


@stats_blueprint.route("/stats/user_count/", methods=["GET"])
def count_users():
    """
    Returns the Amount of Users
    ---
    tags:
        - stats
    responses:
        200:
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            total:
                                type: integer
                            hackers:
                                type: integer
                            sponsors:
                                type: integer
    """
    user_count = User.objects.count()
    hacker_count = Hacker.objects.count()
    sponsor_count = Sponsor.objects.count()

    res = {
        "total": user_count,
        "hackers": hacker_count,
        "sponsors": sponsor_count
    }
    return res, 200
