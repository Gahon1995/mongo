from mongoengine import *
from db.mongodb import BaseDB

from .User import User
from .Article import Article


class Read(BaseDB):
    timestamp = StringField()
    uid = ReferenceField(User)
    aid = ReferenceField(Article)
    readOrNot = StringField()
    readTimeLength = StringField()
    readSequence = StringField()
    agreeOrNot = StringField()
    commentOrNot = StringField()
    shareOrNot = StringField()
    commentDetail = StringField()
