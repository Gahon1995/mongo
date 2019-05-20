#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 00:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from db.mongodb import BaseDB
from mongoengine.fields import *


class Ids(BaseDB):
    ids = SequenceField(required=True, default=0)
    uid = SequenceField(required=True, default=0)
    aid = SequenceField(required=True, default=0)
    rid = SequenceField(required=True, default=0)
    bid = SequenceField(required=True, default=0)
    pid = SequenceField(required=True, default=0)
