from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime

from .User import User
from .Article import Article


class Read(BaseDB):
    uid = ReferenceField(User, required=True)
    aid = ReferenceField(Article, required=True)
    readOrNot = IntField(default=1)
    readTimeLength = IntField(default=0)
    readSequence = IntField(default=1)
    agreeOrNot = IntField(default=0)
    commentOrNot = IntField(default=0)
    shareOrNot = IntField(default=0)
    commentDetail = StringField(default='')
    timestamp = StringField(required=True, default=str(int(datetime.now().timestamp() * 1000)))
