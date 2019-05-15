from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime

from .user import User
from .article import Article

from utils.consts import Region


class Read(BaseDB):
    meta = {
        'indexes': [
            'rid',
            'uid',
            'aid',
            ('aid', 'uid'),
            ('aid', 'readOrNot'),
            ('aid', 'agreeOrNot'),
            ('aid', 'commentOrNot'),
            ('aid', 'shareOrNot'),
        ]
    }

    rid = IntField(required=True, unique=True)
    uid = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)
    aid = ReferenceField(Article, required=True, reverse_delete_rule=NULLIFY)
    readOrNot = IntField(default=1)
    readTimeLength = IntField(default=0)
    readSequence = IntField(default=1)
    agreeOrNot = IntField(default=0)
    commentOrNot = IntField(default=0)
    shareOrNot = IntField(default=0)
    commentDetail = StringField(default='')

    # timestamp = DateTimeField(default=datetime.now)
    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()

    @classmethod
    def new_read(cls, user):
        self = cls()
        self.uid = user

        _id = Read.get_id('rid')
        if user.region == Region.bj:
            self.rid = _id if _id % 2 == 0 else _id + 1
        else:
            self.rid = _id if _id % 2 == 1 else _id + 1
        return self
