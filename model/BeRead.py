#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-03 14:22
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from datetime import datetime

from mongoengine import *

from db.mongodb import BaseDB
from model.Article import Article
from model.User import User


class BeRead(BaseDB):
    # 可以尝试使用LazyReferenceField，看能否优化查询性能

    meta = {
        'indexes': [
            # 'rid',
            'aid',
            'readNum',
            'commentNum',
            'agreeNum',
            'shareNum'
        ]
    }

    # rid = IntField(required=True, unique=True, primary_key=True)
    aid = ReferenceField(Article, required=True, reverse_delete_rule=NULLIFY)
    readNum = IntField(default=0)
    readUidList = ListField(ReferenceField(User, reverse_delete_rule=NULLIFY))
    commentNum = IntField(default=0)
    commentUidList = ListField(ReferenceField(User, reverse_delete_rule=NULLIFY))
    agreeNum = IntField(default=0)
    agreeUidList = ListField(ReferenceField(User, reverse_delete_rule=NULLIFY))
    shareNum = IntField(default=0)
    shareUidList = ListField(ReferenceField(User, reverse_delete_rule=NULLIFY))
    # create_time = DateTimeField(default=datetime.now)
    last_update_time = DateTimeField(default=datetime.utcnow)

    @property
    def create_time(self):
        # 创建时间
        return self.get_create_time()

    def __init__(self, aid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aid = aid

    @classmethod
    def add_read_record(cls, read):

        record = cls.get(aid=read.aid)
        if record is None:
            record = BeRead(read.aid)

        user = read.uid
        if read.readOrNot:
            record.readNum += 1
            if user not in record.readUidList:
                record.readUidList.append(user)
        if read.commentOrNot:
            record.commentNum += 1
            if user not in record.commentUidList:
                record.commentUidList.append(user)
        if read.agreeOrNot:
            record.agreeNum += 1
            if user not in record.agreeUidList:
                record.agreeUidList.append(user)
        if read.shareOrNot:
            record.shareNum += 1
            if user not in record.shareUidList:
                record.shareUidList.append(user)

        record.last_update_time = datetime.utcnow()
        record.save()

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
