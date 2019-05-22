from mongoengine import *

from db.mongodb import BaseDB


class Article(BaseDB):
    aid = IntField(primary_key=True)  # 通过aid的奇偶来判断存到哪一个数据库上去
    title = StringField(required=True)

    category = StringField(required=True)
    abstract = StringField(required=True)
    articleTags = StringField(required=True)
    authors = StringField(required=True)
    language = StringField(required=True)
    text = StringField(required=True)
    image = StringField()
    video = StringField()
    update_time = DateTimeField(required=True)
    timestamp = IntField(required=True)

    meta = {
        'abstract': True,
        'indexes': [
            # 'aid',
            'title',
            'category',
            # 'articleTags',
            'authors'
        ]
    }
    #
    # @property
    # def create_time(self):
    #     # 创建时间
    #     return self.get_create_time()
