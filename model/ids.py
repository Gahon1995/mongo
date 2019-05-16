#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 00:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from db.mongodb import BaseDB
from mongoengine.fields import *


class Ids(BaseDB):
    ids = IntField(required=True, default=0)
    uid = IntField(required=True, default=0)
    aid = IntField(required=True, default=0)
    rid = IntField(required=True, default=0)
    bid = IntField(required=True, default=0)
    pid = IntField(required=True, default=0)
