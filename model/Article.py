from mongoengine import *
from db.mongodb import BaseDB


class Article(BaseDB):
    timestamp = StringField()
    aid = IntField()
    title = StringField()
    category = StringField()
    abstract = StringField()
    articleTags = StringField()
    authors = StringField()
    language = StringField()
    text = StringField()
    image = StringField()
    video = StringField()
