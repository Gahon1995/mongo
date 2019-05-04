from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime

from .User import User
from .Article import Article


class Read(BaseDB):
    meta = {
        'indexes': [
            'uid',
            'aid',
            ('aid', 'uid'),
            ('aid', 'readOrNot'),
            ('aid', 'agreeOrNot'),
            ('aid', 'commentOrNot'),
            ('aid', 'shareOrNot'),
        ]
    }

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
