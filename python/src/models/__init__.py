# -*- coding: utf-8 -*-
"""
    src.models
    ~~~~~~~~~~
    Define the BaseDocument

    Classes:

        BaseDocument

"""
from src import db


class BaseDocument(db.Document):
    """A Base Class to be inherited by all other Document Classes"""
    meta = {
        "abstract": True
    }

    @classmethod
    def findOne(cls, *args, **kwargs):
        """Finds one document"""
        excludes = kwargs.pop("excludes", [])
        return cls.objects(*args, **kwargs).exclude("id", *excludes).first()

    @classmethod
    def createOne(cls, *args, **kwargs):
        """Creates a new document"""
        doc = cls(*args, **kwargs)
        doc.save()
        return doc
