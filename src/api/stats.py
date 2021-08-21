# -*- coding: utf-8 -*-
"""
    src.api.stats
    ~~~~~~~~~~~~~

    Functions:

        count_users()

"""
from src.api import Blueprint
from src.models.user import User
from src.models.hacker import Hacker


stats_blueprint = Blueprint("stats", __name__)


# @stats_blueprint.route("/stats/user_count/", methods=["GET"])
@stats_blueprint.get("/stats/user_count/")
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
    hacker_count = Hacker.objects.count()

    res = {
        "hackers": hacker_count
    }
    return res, 200
