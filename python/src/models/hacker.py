from datetime import datetime

from src import db
from src.models import BaseDocument

HACKERROLE = ("HACKER", "EVENTORG", "SPONSOR", "MOD", "ADMIN")

class HackerProfile(db.EmbeddedDocument):
    pass

class Hacker(BaseDocument):
    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField(unique=True, required=True)
    school_name = db.StringField()
    email = db.EmailField(unique=True, required=True)
    phone_number = db.StringField()
    resume = db.URLField()
    date = db.DateTimeField(default=datetime.utcnow)
    tracks = db.ListField(db.StringField())
    graduation = db.StringField()
    current_status = db.BooleanField()
    permissions = db.ListField(db.StringField(choices=HACKERROLE), required=True)
    profile = db.EmbeddedDocumentField(HackerProfile)
    password = db.StringField(required=True)
    socials = db.ListField(db.StringField())
    
