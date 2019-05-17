#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-18 00:10
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from test.test_base import TestBase
from utils.func import *


class TestUtils(TestBase):

    def test_get_id_by_region(self):
        new_id = get_id_by_region(34, DBMS.region['values'][0])
        assert new_id == 34

        new_id = get_id_by_region(34, DBMS.region['values'][1])
        assert new_id == 35

        new_id = get_id_by_region(33, DBMS.region['values'][0])
        assert new_id == 34

        pass

    def test_get_dbms_by_uid(self):
        dbms = get_dbms_by_uid(34)
        # print(dbms)
        assert dbms == DBMS.region[DBMS.region['values'][0]]

        dbms = get_dbms_by_uid(35)
        # print(dbms)
        assert dbms == DBMS.region[DBMS.region['values'][1]]

    def test_get_dbms_by_aid(self):
        dbms = get_dbms_by_aid(34)
        # print(dbms)
        assert dbms == DBMS.category[DBMS.category['values'][0]]

        dbms = get_dbms_by_aid(35)
        # print(dbms)
        assert dbms == DBMS.category[DBMS.category['values'][1]]

    def test_get_id_by_category(self):
        new_id = get_id_by_category(34, DBMS.category['values'][0])
        assert new_id == 34

        new_id = get_id_by_category(34, DBMS.category['values'][1])
        assert new_id == 35

        new_id = get_id_by_category(33, DBMS.category['values'][0])
        assert new_id == 34
