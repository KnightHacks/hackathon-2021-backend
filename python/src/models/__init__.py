from src import db

class BaseDocument(db.Document):
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
