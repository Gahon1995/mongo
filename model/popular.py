#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 16:05
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from mongoengine import *

from db.mongodb import BaseDB

temporalChoices = ('daily', 'weekly', 'monthly')


class Popular(BaseDB):
    meta = {
        'abstract': True,
        'indexes': [
            'temporalGranularity',
            'timestamp',
            ('temporalGranularity', 'timestamp')
        ]
    }

    temporalGranularity = StringField(max_length=7, choices=temporalChoices)
    articleAidDict = DictField(default={})
    timestamp = IntField(required=True)
    update_time = IntField(required=True)

    # timestamp = DateTimeField(default=datetime.now)
    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()
