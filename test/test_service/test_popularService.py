#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-19 14:31
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from service.popular_service import PopularService
from test.test_base import TestBase
from utils.func import timestamp_to_datetime


class TestPopularService(TestBase):
    def test_update_popular(self):
        _date = timestamp_to_datetime(1506342197000).date()
        PopularService().update_popular(_date)
