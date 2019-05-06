#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 16:05
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from datetime import datetime

from mongoengine import *

from db.mongodb import BaseDB
from model.article import Article

temporalChoices = ('daily', 'weekly', 'monthly')


class Popular(BaseDB):
    meta = {
        'indexes': [
            'temporalGranularity'
        ]
    }

    # default id _id
    temporalGranularity = StringField(max_length=7, choices=temporalChoices)
    articleAidList = ListField(ReferenceField(Article, reverse_delete_rule=NULLIFY))
    update_time = DateTimeField(default=datetime.utcnow)

    # timestamp = DateTimeField(default=datetime.now)
    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()
