# -*- coding: utf-8 -*-
"""
    src.common.json
    ~~~~~~~~~~~~~~~
    Overrides Flask's and Mongoengine's json encoders

    Classes:

        JSONEncoderBase

"""
import datetime
from flask.json import JSONEncoder
from mongoengine.base import BaseDocument
from mongoengine.queryset import QuerySet
from src.models.user import ROLES
from bson.objectid import ObjectId


class JSONEncoderBase(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, ROLES):
                return [r.name for r in ROLES if r & obj]
            elif isinstance(obj, BaseDocument):
                return obj.to_mongo(use_db_field=False)
            elif isinstance(obj, QuerySet):
                return list(obj)
            elif isinstance(obj, ObjectId):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
