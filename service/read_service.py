#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from bson import ObjectId
import datetime

from model.read import Read
from model.be_read import BeRead
from utils.consts import DBMS, Category, Region
from utils.func import check_alias
from db.mongodb import switch_mongo_db
import logging

from utils.func import utc_2_local, sort_dict, get_dbms_by_category, get_dbms_by_region, merge_dict_and_sort

logger = logging.getLogger('ReadService')


class ReadService(object):

    @staticmethod
    def get_be_id():
        return max(ReadService.__be_id(DBMS.DBMS1), ReadService.__be_id(DBMS.DBMS2))

    @staticmethod
    @switch_mongo_db(cls=BeRead, default_db=DBMS.DBMS2)
    def __be_id(db_alias=None):
        check_alias(db_alias)
        return BeRead.get_id('bid')

    @staticmethod
    @switch_mongo_db(cls=Read)
    def count(db_alias=None, **kwargs):
        check_alias(db_alias)
        return Read.count(**kwargs)

    @staticmethod
    def save_read(new_read):
        logger.info('save read:{}'.format(new_read))

        ReadService.__save_read(new_read, db_alias=get_dbms_by_region(new_read.uid.region))

        for dbms in get_dbms_by_category(new_read.aid.category):
            ReadService.__save_be_read(new_read, db_alias=dbms)

    @staticmethod
    def __save_read(read, db_alias=None):
        check_alias(db_alias)
        read.save()

    @staticmethod
    @switch_mongo_db(cls=BeRead)
    def __save_be_read(new_read, db_alias=None):
        check_alias(db_alias)
        _id = ReadService.get_be_id()

        if new_read.aid.category == Category.science:
            bid = _id if _id % 2 == 0 else _id + 1
        else:
            bid = _id if _id % 2 == 1 else _id + 1

        return BeRead.add_read_record(new_read, bid)

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
        if isinstance(end_date, datetime.date) and not isinstance(end_date, datetime.datetime):
            end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')
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
