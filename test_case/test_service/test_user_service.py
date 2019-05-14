#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-14 13:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from test_case.base_test import TestBase
from service.user_service import UserService
from utils.consts import Region


class TestUserService(TestBase):

    def test_user_list(self):
        users = UserService.users_list(db_alias=Region.hk)
        UserService.pretty_users(users)
