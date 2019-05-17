#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 23:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com


from model.be_read import BeRead
from model.ids import Ids

from db.mongodb import switch_mongo_db
import logging

from service.ids_service import IdsService
from utils.func import *

from service.article_service import ArticleService

logger = logging.getLogger('ReadService')


class BeReadService(object):

    @staticmethod
    @switch_mongo_db(cls=BeRead)
    def get_by_aid(aid, db_alias=None):
        check_alias(db_alias)
        return BeRead.get(aid=aid)

    @staticmethod
    def get_be_id():
        return IdsService().next_id('bid')
        # return max(BeReadService.__be_id(DBMS.DBMS1), BeReadService.__be_id(DBMS.DBMS2))

    @staticmethod
    @switch_mongo_db(cls=BeRead, default_db=DBMS.DBMS2)
    def __be_id(db_alias=None):
        check_alias(db_alias)
        return BeRead.get_id('bid')

    @staticmethod
    def add_be_read_record(aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, region, timestamp=None):

        _id = BeReadService.get_be_id()
        bid = get_id_by_region(_id, region)

        article = ArticleService().get_article_by_aid(aid)

        for dbms in get_dbms_by_category(article.category):
            BeReadService.save_new_be_read(bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot,
                                           timestamp, db_alias=dbms)
        IdsService().set_id('bid', bid)

    @staticmethod
    @switch_mongo_db(cls=BeRead)
    def save_new_be_read(bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp=None, db_alias=None):
        check_alias(db_alias)

        be_read = BeReadService.get_by_aid(aid, db_alias=db_alias)
        if be_read is None:
            be_read = BeRead()
            be_read.aid = aid
            be_read.bid = bid
            be_read.timestamp = timestamp or datetime.datetime.utcnow()

        if readOrNot:
            be_read.readNum += 1
            if uid not in be_read.readUidList:
                be_read.readUidList.append(uid)
        if commentOrNot:
            be_read.commentNum += 1
            if uid not in be_read.commentUidList:
                be_read.commentUidList.append(uid)
        if agreeOrNot:
            be_read.agreeNum += 1
            if uid not in be_read.agreeUidList:
                be_read.agreeUidList.append(uid)
        if shareOrNot:
            be_read.shareNum += 1
            if uid not in be_read.shareUidList:
                be_read.shareUidList.append(uid)

        be_read.last_update_time = datetime.datetime.utcnow()
        be_read.save()
