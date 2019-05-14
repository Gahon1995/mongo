#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-06 16:20
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.popular import Popular
from service.read_service import ReadService
from db.mongodb import switch_mongo_db
import datetime


class PopularService(object):

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def get_daily_rank(db_alias=None):
        return Popular.get(temporalGranularity='daily')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def get_weekly_rank(db_alias=None):
        return Popular.get(temporalGranularity='weekly')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def get_monthly_rank(db_alias=None):
        return Popular.get(temporalGranularity='monthly')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def _update_rank(rank, articles, temporal, db_alias=None):
        if rank is None:
            rank = Popular()
            rank.temporalGranularity = temporal
        rank.articleAidList.clear()
        for article in articles:
            rank.articleAidList.append(article[0])

        rank.update_time = datetime.datetime.utcnow()
        rank.save()

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def update_daily_rank(db_alias=None):
        rank = PopularService.get_daily_rank()
        articles = ReadService.get_daily_popular(datetime.datetime.now())
        PopularService._update_rank(rank, articles, 'daily')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def update_weekly_rank(db_alias=None):
        rank = PopularService.get_weekly_rank()
        articles = ReadService.get_weekly_popular(datetime.datetime.now())
        PopularService._update_rank(rank, articles, 'weekly')

    @staticmethod
    @switch_mongo_db(cls=Popular)
    def update_monthly_rank(db_alias=None):
        rank = PopularService.get_monthly_rank()
        articles = ReadService.get_month_popular(datetime.datetime.now())
        PopularService._update_rank(rank, articles, 'monthly')
