#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from bson import ObjectId
import datetime

from model.read import Read
from model.be_read import BeRead
from service.article_service import ArticleService
from db.mongodb import switch_mongo_db
import logging

from utils.func import utc_2_local, sort_dict

logger = logging.getLogger('ReadService')


class ReadService(object):

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_size(db_alias=None, **kwargs):
        return Read.count(**kwargs)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def save_new_read(new_read, db_alias=None):
        logger.info('save read:{}'.format(new_read))
        new_read.save()
        ReadService.__save_new_be_read(new_read, db_alias)

    @staticmethod
    @switch_mongo_db(cls=BeRead)
    def __save_new_be_read(new_read, db_alias=None):
        return BeRead.add_read_record(new_read)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def reads_list(page_num=1, page_size=20, db_alias=None, **kwargs):
        return Read.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def del_read(_id, db_alias=None):
        article = Read.get(id=_id)
        if article is not None:
            article.delete()
            return True
        return False

    @staticmethod
    @switch_mongo_db(cls=Read)
    def read_info(_id, db_alias=None):
        return Read.get(id=_id)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_history(user, page_num=1, page_size=20, db_alias=None):
        return Read.list_by_page(page_num, page_size, uid=user)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_popular(end_date, before_days, top_n, db_alias=None):
        if isinstance(end_date, datetime.date) and not isinstance(end_date, datetime.datetime):
            end_date = datetime.datetime.strptime(str(end_date), '%Y-%m-%d')
        if isinstance(end_date, datetime.datetime):
            # if date.tzinfo is None:
            #     date = utc_2_local(date)
            start = ObjectId.from_datetime(utc_2_local(end_date - datetime.timedelta(days=before_days)))
            end = ObjectId.from_datetime(utc_2_local(end_date))
        else:
            print("查询日期格式不对，需要datetime或date类型")
            return None

        result = Read.objects(id__gt=start, id__lt=end)
        fre = result.item_frequencies('aid')
        # TODO 根据fre排序，然后返回对应的文章标题或阅读信息
        return sort_dict(fre)[:top_n]
        # articles = list()
        # for aid, count in freq:
        #     article = ArticleService.get_an_article(id=aid)
        #     articles.append({'data': article, 'cnt': count})
        # return articles

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_daily_popular(end_date, before_days=1, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_weekly_popular(end_date, before_days=7, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n)

    @staticmethod
    @switch_mongo_db(cls=Read)
    def get_month_popular(end_date, before_days=30, top_n=10, db_alias=None):
        return ReadService.get_popular(end_date, before_days, top_n)
