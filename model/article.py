from datetime import datetime

from mongoengine import *

from db.mongodb import BaseDB


class Article(BaseDB):
    aid = IntField(required=True, unique=True)  # 通过aid的奇偶来判断存到哪一个数据库上去
    title = StringField(required=True)

    category = StringField(required=True)
    abstract = StringField(required=True)
    articleTags = StringField(required=True)
    authors = StringField(required=True)
    language = StringField(required=True)
    text = StringField(required=True)
    image = StringField(default='')
    video = StringField(default='')
    update_time = DateTimeField(default=datetime.utcnow)
    timestamp = IntField(required=True)

    meta = {
        'abstract': True,
        'indexes': [
            'aid',
            'title',
            'category',
            'articleTags',
            'authors',
            'language'
        ]
    }

    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()
