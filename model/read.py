from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime


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
    uid = IntField(required=True)
    aid = IntField(required=True)
    readOrNot = IntField(default=1)
    readTimeLength = IntField(default=0)
    readSequence = IntField(default=1)
    agreeOrNot = IntField(default=0)
    commentOrNot = IntField(default=0)
    shareOrNot = IntField(default=0)
    commentDetail = StringField(default='')

    timestamp = DateTimeField(default=datetime.utcnow)

    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()
