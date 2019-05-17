#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 23:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com


from model.be_read import BeRead

from db.mongodb import switch_mongo_db
import logging

from service.ids_service import IdsService
from utils.func import *

from service.article_service import ArticleService

logger = logging.getLogger('ReadService')


@singleton
class BeReadService(object):
    field_names = ['bid', "aid", "readNum", "readUidList", "commentNum", "commentUidList", "agreeNum", "agreeUidList",
                   "shareNum", "shareUidList", "timestamp", "last_update_time"]

    @staticmethod
    def get_bid():
        return IdsService().next_id('bid')
        # return max(BeReadService.__be_id(DBMS.DBMS1), BeReadService.__be_id(DBMS.DBMS2))

    @switch_mongo_db(cls=BeRead, allow_None=True)
    def get_by_aid(self, aid, db_alias=None):
        if db_alias is None:
            return self.get_by_aid(aid, db_alias=get_best_dbms_by_aid(aid))
        else:
            check_alias(db_alias)
            return BeRead.get(aid=aid)

    @switch_mongo_db(cls=BeRead, allow_None=True)
    def get_by_bid(self, bid, db_alias=None):
        if db_alias is None:
            be_read = None
            for dbms in DBMS.all:
                be_read = self.get_by_bid(bid, db_alias=dbms)
                if be_read is not None:
                    break
            return be_read
        else:
            check_alias(db_alias)
            return BeRead.get(bid=bid)

    # @switch_mongo_db(cls=BeRead)
    # def __be_id(self, db_alias=None):
    #     check_alias(db_alias)
    #     return BeRead.get_id('bid')

    def add_be_read_record(self, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp=None):

        _id = self.get_bid()
        article = ArticleService().get_article_by_aid(aid)
        if article is None:
            return None
        bid = get_id_by_category(_id, article.category)

        be_read = None
        for dbms in get_dbms_by_category(article.category):
            logger.info("save be read to : {} uid: {}".format(dbms, uid))
            be_read = self.__save_be_read(bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot,
                                          timestamp, db_alias=dbms)
        IdsService().set_id('bid', bid)
        return be_read

    @switch_mongo_db(cls=BeRead)
    def __save_be_read(self, bid, aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp=None,
                       db_alias=None):
        check_alias(db_alias)

        be_read = self.get_by_aid(aid, db_alias=db_alias)
        if be_read is None:
            be_read = BeRead()
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

    @switch_mongo_db(cls=BeRead)
    def __get_popular(self, top_n=20, db_alias=None, **kwargs):
        check_alias(db_alias)
        return BeRead.objects(**kwargs).order_by('-aid').limit(top_n)
        pass
