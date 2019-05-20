#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 23:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com


# from model.be_read import BeRead

import logging

from model.be_read import BeRead
from service.article_service import ArticleService
from service.ids_service import IdsService
from utils.func import *

logger = logging.getLogger('ReadService')


@singleton
class BeReadService(object):
    field_names = ["aid", "readNum", "readUidList", "commentNum", "commentUidList", "agreeNum", "agreeUidList",
                   "shareNum", "shareUidList", "timestamp", "last_update_time"]

    @staticmethod
    def get_model(dbms: str):
        class Model(BeRead):
            meta = {
                'db_alias': dbms,
                'collection': 'be_read'
            }
            pass

        return Model

    @staticmethod
    def get_bid():
        return IdsService().next_id('bid')

    def get_by_aid(self, aid: str, db_alias=None):
        if db_alias is None:
            article = ArticleService().get_an_article_by_aid(aid)
            return self.get_by_aid(aid, db_alias=get_best_dbms_by_category(article.category))
        else:
            check_alias(db_alias)
            return self.get_model(db_alias).get(aid=aid)

    def add_be_read_record(self, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp=None):

        article = ArticleService().get_an_article_by_aid(aid)
        if article is None:
            return None

        be_read = self.get_by_aid(aid)
        bid = self.get_bid() if be_read is None else be_read.bid
        for dbms in get_dbms_by_category(article.category):
            logger.info("save be read to : {} uid: {}".format(dbms, uid))
            be_read = self.__save_be_read(bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp,
                                          db_alias=dbms)

        return be_read

    def __save_be_read(self, bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp=None,
                       db_alias=None):
        check_alias(db_alias)

        be_read = self.get_by_aid(aid, db_alias=db_alias)
        if be_read is None:
            be_read = self.get_model(db_alias)()
            be_read.aid = aid
            be_read.bid = bid
            be_read.timestamp = timestamp or get_timestamp()

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
        return be_read

    def get_total_popular(self, top_n=20, **kwargs):
        popular = list()
        aids = list()
        for dbms in DBMS.all:
            logger.info("get_total_popular on {}".format(dbms))
            pop = self.__get_popular(top_n, db_alias=dbms, **kwargs)

            for p in pop:
                if p.aid not in aids:
                    popular.append(p)
                    aids.append(p.aid)

        return sort_dict_in_list(popular, 'readNum')[:top_n]
        pass

    def __get_popular(self, top_n=20, db_alias=None, **kwargs):
        check_alias(db_alias)
        return self.get_model(db_alias).objects(**kwargs).order_by('-aid').limit(top_n)
        pass
