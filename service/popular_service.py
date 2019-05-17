#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-06 16:20
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.popular import Popular
from service.read_service import ReadService
from db.mongodb import switch_mongo_db
import datetime
from config import DBMS


class PopularService(object):

    @staticmethod
    @switch_mongo_db(cls=Popular, default_db=DBMS.DBMS1)
    def get_daily_rank(end_date, db_alias=DBMS.DBMS1):
        return Popular.get(update_time=end_date, temporalGranularity='daily')

    @staticmethod
    @switch_mongo_db(cls=Popular, default_db=DBMS.DBMS1)
    def get_weekly_rank(end_date, db_alias=DBMS.DBMS1):
        return Popular.get(update_time=end_date, temporalGranularity='weekly')

    @staticmethod
    @switch_mongo_db(cls=Popular, default_db=DBMS.DBMS1)
    def get_monthly_rank(end_date, db_alias=DBMS.DBMS1):
        return Popular.get(update_time=end_date, temporalGranularity='monthly')

    @staticmethod
    @switch_mongo_db(cls=Popular, default_db=DBMS.DBMS1)
    def _update_rank(rank, articles, temporal, db_alias=DBMS.DBMS1):
        if rank is None:
            rank = Popular()
            rank.temporalGranularity = temporal
        rank.articleAidList.clear()
        for article in articles:
            rank.articleAidList.append(article[0])

        rank.update_time = datetime.date.today()
        rank.save()

    @staticmethod
    @switch_mongo_db(cls=Popular, default_db=DBMS.DBMS1)
    def update_daily_rank(today, db_alias=DBMS.DBMS1):
        rank = PopularService().get_daily_rank(today)
        articles = ReadService().get_daily_popular(today)
        PopularService._update_rank(rank, articles, 'daily')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def update_weekly_rank(today, db_alias=DBMS.DBMS1):
        rank = PopularService().get_weekly_rank(today)
        articles = ReadService().get_weekly_popular(today)
        PopularService._update_rank(rank, articles, 'weekly')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def update_monthly_rank(today, db_alias=DBMS.DBMS1):
        rank = PopularService().get_monthly_rank(today)
        articles = ReadService().get_month_popular(today)
        PopularService._update_rank(rank, articles, 'monthly')

    @staticmethod
    def update_popular(_date=None):
        _date = _date or datetime.date.today()
        PopularService.update_daily_rank(_date)
        PopularService.update_monthly_rank(_date)
        PopularService.update_weekly_rank(_date)
        pass
