# -*- coding: utf-8 -*-
"""
    src.common.error_handlers
    ~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from flask import json


def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""

    response = e.get_response()

    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response
