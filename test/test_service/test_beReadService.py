#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-17 23:48
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from config import DBMS
from service.be_read_service import BeReadService
from test.test_base import TestBase


class TestBeReadService(TestBase):

    def setup_method(self) -> None:
        self.beReadService = BeReadService()

    def test_get_be_id(self):
        bid = self.beReadService.get_bid()
        print(bid)

    def test_get_by_aid(self):
        beread = self.beReadService.get_by_aid(1)
        print(beread)
        beread = self.beReadService.get_by_aid(6)
        print(beread)

    def test_get_by_bid(self):
        be = self.beReadService.get_by_bid(1)
        print(be)

        be = self.beReadService.get_by_bid(2)
        print(be)

    def test_add_be_read_record(self):
        # 该方法在测试添加read记录时会自动测试
        pass

    def test_get_total_popular(self):
        from utils.func import pretty_models
        populars = self.beReadService.get_total_popular()
        pretty_models(populars, self.beReadService.field_names)
