#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-05 12:49
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from utils.func import singleton
from service.user_service import UserService


@singleton
class UserController(object):

    @staticmethod
    def login(username, password, is_admin=False):
        if is_admin and username != "admin":
            return None
        return UserService.login(username, password)

    @staticmethod
    def query_all(page_num=1, page_size=20, **kwargs):
        # total_pages = int((total - 1) / page_size) + 1
        # print("\n" + "=" * 20)
        users = UserService.users_list(page_num, page_size, **kwargs)
        UserService.pretty_users(users)
