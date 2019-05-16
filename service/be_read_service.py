#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 23:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com


from model.be_read import BeRead

from db.mongodb import switch_mongo_db
import logging

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
        return max(BeReadService.__be_id(DBMS.DBMS1), BeReadService.__be_id(DBMS.DBMS2))

    @staticmethod
    @switch_mongo_db(cls=BeRead, default_db=DBMS.DBMS2)
    def __be_id(db_alias=None):
        check_alias(db_alias)
        return BeRead.get_id('bid')

    @staticmethod
    def add_be_read_record(read, user):

        _id = BeReadService.get_be_id()
        bid = get_id_by_region(_id, user.region)

        article = ArticleService.get_article_by_aid(read.aid)

        for dbms in get_dbms_by_category(article.category):
            record = BeReadService.get_by_aid(read.aid, db_alias=dbms)
            if record is None:
                record = BeRead()
                record.aid = read.aid
                record.bid = bid
            BeReadService.save_new_be_read(record, read, user.uid, db_alias=dbms)

    @staticmethod
    @switch_mongo_db(cls=BeRead)
    def save_new_be_read(be_read, read, uid, db_alias=None):
        check_alias(db_alias)

        if read.readOrNot:
            be_read.readNum += 1
            if uid not in be_read.readUidList:
                be_read.readUidList.append(uid)
        if read.commentOrNot:
            be_read.commentNum += 1
            if uid not in be_read.commentUidList:
                be_read.commentUidList.append(uid)
        if read.agreeOrNot:
            be_read.agreeNum += 1
            if uid not in be_read.agreeUidList:
                be_read.agreeUidList.append(uid)
        if read.shareOrNot:
            be_read.shareNum += 1
            if uid not in be_read.shareUidList:
                be_read.shareUidList.append(uid)

        be_read.last_update_time = datetime.utcnow()
        be_read.save()
