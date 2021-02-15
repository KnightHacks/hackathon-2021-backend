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


stats_blueprint = Blueprint("stats", __name__)


@stats_blueprint.route("/stats/usercount", methods=["GET"])
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
    """
    user_count = User.objects.count()
    hacker_count = Hacker.objects.count()

    res = {
        "total": user_count,
        "hackers": hacker_count
    }
    return res, 200
