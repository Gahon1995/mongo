from mongoengine import *
from db.mongodb import BaseDB


class User(BaseDB):
    timestamp = StringField()
    uid = IntField()
    name = StringField()
    gender = StringField()
    email = StringField()
    phone = StringField()
    dept = StringField()
    grade = StringField()
    language = StringField()
    region = StringField()
    role = StringField()
    preferTags = StringField()
    obtainedCredits = IntField()












