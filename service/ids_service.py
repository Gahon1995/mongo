#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 01:04
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.ids import Ids
from config import DBMS
from db.mongodb import switch_mongo_db
from utils.func import check_alias
import logging

logger = logging.getLogger('IdsService')


class IdsService(object):

    def init(self):
        ids = Ids()
        ids.ids = 0
        ids.uid = 0
        ids.aid = 0
        ids.rid = 0
        ids.bid = 0
        ids.pid = 0
        ids.save()
        return ids

    def next_id(self, name):
        ids = Ids.get(ids=0)
        if ids is None:
            ids = self.init()
        logger.debug('set {}: {}'.format(name, getattr(ids, name)))
        return getattr(ids, name)

    def set_id(self, name, last_id):
        for dbms in DBMS.all:
            self.__set_id(name, last_id, db_alias=dbms)

    @switch_mongo_db(cls=Ids)
    def __set_id(self, name, last_id, db_alias=None):
        check_alias(db_alias=db_alias)
        logger.debug('set {}: {}'.format(name, last_id + 1))
        ids = Ids.get(ids=0)
        if ids is None:
            ids = IdsService().init()
        setattr(ids, name, last_id + 1)
        ids.save()
