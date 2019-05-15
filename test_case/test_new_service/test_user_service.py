#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 16:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from test_case.base_test import TestBase

from Config import Config

from new_service.user_service import UserService
from utils.func import *


class TestUserService(TestBase):
    pass

    def test_users_list(self):
        bj_service = UserService(get_dbms_location('User', 'Beijing'))
        bj_service.get_users()
        pass
