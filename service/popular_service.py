#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-06 16:20
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

import datetime
import logging
import threading

from config import DBMS
from model.popular import Popular
from service.article_service import ArticleService
from service.read_service import ReadService
from utils.func import date_to_timestamp, get_timestamp, check_alias

logger = logging.getLogger('PopularService')


class PopularService(object):
    field_names = []

    @staticmethod
    def get_model(dbms: str):
        class Model(Popular):
            meta = {
                'db_alias': dbms,
                'collection': 'popular'
            }
            pass

        return Model

    def __update_rank(self, rank, articles, db_alias):
        rank.articleAidDict = {}
        for aid, count in articles:
            if ArticleService().has_article(aid, db_alias):
                rank.articleAidDict[str(aid)] = count

        rank.update_time = get_timestamp()
        rank.save()

    def __update_daily_rank(self, articles, _date, db_alias):
        rank = self.get_daily_rank(_date, db_alias)
        if rank is None:
            rank = self.get_model(db_alias)()
            rank.timestamp = date_to_timestamp(_date)
            rank.temporalGranularity = 'daily'
            logger.info(
                "thread: {} create new daily popular on {}, at {}".format(threading.current_thread(), db_alias, _date))
        self.__update_rank(rank, articles, db_alias)

    def __update_weekly_rank(self, articles, _date, db_alias):
        rank = self.get_weekly_rank(_date, db_alias)
        if rank is None:
            rank = self.get_model(db_alias)()
            rank.timestamp = date_to_timestamp(_date)
            rank.temporalGranularity = 'weekly'
        self.__update_rank(rank, articles, db_alias)

    def __update_monthly_rank(self, articles, _date, db_alias):
        rank = self.get_monthly_rank(_date, db_alias)
        if rank is None:
            rank = self.get_model(db_alias)()
            rank.timestamp = date_to_timestamp(_date)
            rank.temporalGranularity = 'monthly'
        self.__update_rank(rank, articles, db_alias)

    def update_popular(self, _date=None, db_alias=None, daily_pop=None, weekly_pop=None, monthly_pop=None):
        if isinstance(_date, datetime.datetime):
            _date = _date.date()
        _date = _date or datetime.date.today()
        if daily_pop is None:
            daily_pop = ReadService().get_daily_popular(_date)
            weekly_pop = ReadService().get_weekly_popular(_date)
            monthly_pop = ReadService().get_monthly_popular(_date)
        if db_alias is None:
            for dbms in DBMS.all:
                self.update_popular(_date=_date, db_alias=dbms,
                                    daily_pop=daily_pop,
                                    weekly_pop=weekly_pop,
                                    monthly_pop=monthly_pop)
            pass
        else:

            check_alias(db_alias)

            self.__update_daily_rank(daily_pop, _date, db_alias)
            self.__update_monthly_rank(weekly_pop, _date, db_alias)
            self.__update_weekly_rank(monthly_pop, _date, db_alias)

            logger.info("update popular on {}, date:{}".format(db_alias, _date))
            pass

    def get_daily_rank(self, _date, db_alias):
        return self.get_model(db_alias).get(timestamp=date_to_timestamp(_date), temporalGranularity='daily')

    def get_weekly_rank(self, _date, db_alias):
        return self.get_model(db_alias).get(timestamp=date_to_timestamp(_date), temporalGranularity='weekly')

    def get_monthly_rank(self, _date, db_alias):
        return self.get_model(db_alias).get(timestamp=date_to_timestamp(_date), temporalGranularity='monthly')
