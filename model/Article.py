from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime


class Article(BaseDB):
    aid = IntField(required=True, unique=True)
    title = StringField(required=True)
    category = StringField(required=True)
    abstract = StringField(required=True)
    articleTags = StringField(required=True)
    authors = StringField(required=True)
    language = StringField(required=True)
    text = StringField(default='')
    image = StringField(default='')
    video = StringField(default='')
    timestamp = StringField(required=True, default=str(int(datetime.now().timestamp() * 1000)))
