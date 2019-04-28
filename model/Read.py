from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime

from .User import User
from .Article import Article


class Read(BaseDB):
    uid = ReferenceField(User, required=True)
    aid = ReferenceField(Article, required=True)
    readOrNot = StringField(default=0)
    readTimeLength = StringField(default=0)
    readSequence = StringField(default=0)
    agreeOrNot = StringField(default=0)
    commentOrNot = StringField(default=0)
    shareOrNot = StringField(default=0)
    commentDetail = StringField(default='')
    timestamp = StringField(required=True, default=str(int(datetime.now().timestamp() * 1000)))
