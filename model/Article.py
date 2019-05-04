from mongoengine import *
from db.mongodb import BaseDB
from datetime import datetime


class Article(BaseDB):
    # aid = IntField(primary_key=True)
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

    meta = {
        'indexes': [
            # 'aid',
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

    # timestamp = DateTimeField(default=datetime.now)

    @classmethod
    def search_by_title(cls, name):
        # TODO 测试该方法是否有用
        return cls.objects(title_contains=name)
