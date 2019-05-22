#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 14:22
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from datetime import datetime

from mongoengine import *

from db.mongodb import BaseDB


class BeRead(BaseDB):
    # 可以尝试使用LazyReferenceField，看能否优化查询性能

    meta = {
        'abstract': True,
        'indexes': [
            # 'bid',
            'aid',
            # 'readNum',
            # 'commentNum',
            # 'agreeNum',
            # 'shareNum'
        ]
    }

    bid = IntField(primary_key=True)
    aid = IntField(required=True, unique=True)
    readNum = IntField(default=0)
    readUidList = ListField(IntField(required=False), default=list())
    commentNum = IntField(default=0)
    commentUidList = ListField(IntField(required=False), default=list())
    agreeNum = IntField(default=0)
    agreeUidList = ListField(IntField(required=False), default=list())
    shareNum = IntField(default=0)
    shareUidList = ListField(IntField(required=False), default=list())
    timestamp = IntField(required=True)
    last_update_time = DateTimeField(default=datetime.utcnow)

    # @property
    # def create_time(self):
    #     # 创建时间
    #     return self.get_create_time()

    @classmethod
    def add_read_record(cls, read):
        pass

    def never_read(self, user):
        return user not in self.readUidList

    def never_comment(self, user):
        if user not in self.commentUidList:
            return True
        else:
            return False

    def never_agree(self, user):
        if user not in self.agreeUidList:
            return True
        else:
            return False

    def never_share(self, user):
        if user not in self.shareUidList:
            return True
        else:
            return False

    @classmethod
    def get_top_read(cls, num=10):
        return cls.objects.order_by('-readNum').limit(num)

    @classmethod
    def get_top_comment(cls, num=10):
        return cls.objects.order_by('-commentNum').limit(num)

    @classmethod
    def get_top_agree(cls, num=10):
        return cls.objects.order_by('-agreeNum').limit(num)

    @classmethod
    def get_top_share(cls, num=10):
        return cls.objects.order_by('-shareNum').limit(num)
