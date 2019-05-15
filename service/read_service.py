#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from bson import ObjectId
import datetime

from model.read import Read
from utils.func import *
from db.mongodb import switch_mongo_db
import logging

from service.be_read_service import BeReadService
from service.user_service import UserService

logger = logging.getLogger('ReadService')


class ReadService(object):

    @staticmethod
    def get_id():
        _id = -1
        for dbms in DBMS.all:
            _id = max(ReadService.__id(db_alias=dbms), _id)
        return _id

    @staticmethod
    @switch_mongo_db(cls=Read)
    def __id(db_alias=None):
        check_alias(db_alias)
        return Read.get_id('rid')

    @staticmethod
    @switch_mongo_db(cls=Read)
    def count(db_alias=None, **kwargs):
        check_alias(db_alias)
        return Read.count(**kwargs)

    @staticmethod
    def save_read(aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot, commentDetail, agreeOrNot,
                  shareOrNot):
        # logger.info('save read:{}'.format(new_read))

        user = UserService.get_user_by_uid(int(uid))
        _id = ReadService.get_id()
        rid = get_id_by_region(_id, user.region)

        new_read = None
        for dbms in get_dbms_by_uid(uid):
            new_read = ReadService.__save_read(rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot,
                                               commentDetail,
                                               agreeOrNot,
                                               shareOrNot, db_alias=dbms)

        BeReadService.add_be_read_record(new_read, user)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def __save_read(rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot, commentDetail, agreeOrNot,
                    shareOrNot, db_alias=None):
        check_alias(db_alias)

        new_read = Read()
        new_read.rid = rid
        new_read.aid = aid
        new_read.uid = uid
        new_read.readOrNot = int(readOrNot)
        new_read.readTimeLength = int(readTimeLength)
        new_read.readSequence = int(readSequence)
        new_read.commentOrNot = int(commentOrNot)
        new_read.commentDetail = commentDetail
        new_read.agreeOrNot = int(agreeOrNot)
        new_read.shareOrNot = int(shareOrNot)
        logger.info("save to dbms:{}\nrecord: {}".format(db_alias, new_read))
        new_read.save()
        return new_read

    @staticmethod
    @switch_mongo_db(cls=Read)
    def reads_list(page_num=1, page_size=20, db_alias=None, **kwargs):
        check_alias(db_alias)
        return Read.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def del_read(_id, db_alias=None):
        check_alias(db_alias)
        article = Read.objects(id=_id).first()
        if article is not None:
            article.delete()
            # return True
        return True

    @staticmethod
    @switch_mongo_db(cls=Read)
    def read_info(_id, db_alias=None):
        check_alias(db_alias)
        return Read.objects(id=_id).first()

    @staticmethod
    def get_history(user, page_num=1, page_size=20):
        # TODO 当DBMS1 节点查询出错时， 选择DBMS2 节点
        return ReadService.__get_history(user, page_num, page_size, db_alias=get_dbms_by_region(user.region))

    @staticmethod
    @switch_mongo_db(cls=Read)
    def __get_history(user, page_num=1, page_size=20, db_alias=None):
        check_alias(db_alias)
        return Read.list_by_page(page_num, page_size, uid=user)

    @staticmethod
    def get_popular(end_date, before_days, top_n=5, db_alias=None):
        if isinstance(end_date, datetime.date):
            end_date = datetime.datetime.strptime(
                str("{}-{}-{}".format(end_date.year, end_date.month, end_date.day + 1)), '%Y-%m-%d')
        if isinstance(end_date, datetime.datetime):
            start = ObjectId.from_datetime(utc_2_local(end_date - datetime.timedelta(days=before_days)))
            end = ObjectId.from_datetime(utc_2_local(end_date))
        else:
            print("查询日期格式不对，需要datetime或date类型")
            return None
        if db_alias is None:
            fre1 = ReadService.__get_popular(start, end, db_alias=DBMS.DBMS1)
            fre2 = ReadService.__get_popular(start, end, db_alias=DBMS.DBMS2)

            # TODO 测试结果正确性
            return merge_dict_and_sort(fre1, fre2)[:top_n]
        else:
            fre = ReadService.__get_popular(start, end, db_alias=db_alias)
            return sort_dict(fre)[:top_n]

    @staticmethod
    def __get_popular(start, end, db_alias=None):
        check_alias(db_alias)
        return Read.objects(id__gt=start, id__lt=end).item_frequencies('aid')
        pass

    @staticmethod
    def get_daily_popular(end_date, before_days=1, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n, db_alias=db_alias)

    @staticmethod
    def get_weekly_popular(end_date, before_days=7, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n, db_alias=db_alias)

    @staticmethod
    def get_month_popular(end_date, before_days=30, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n, db_alias=db_alias)
