#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 15:55
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from dao.user_dao import UserDao
from model.user import User
from utils.func import check_alias

from mongoengine.context_managers import switch_db


class UserService(object):

    def __init__(self, dbms):
        self.model = User
        self.DBMS = dbms
        self.dao = UserDao()
        check_alias(dbms)

    @staticmethod
    def hasattr(key):
        return hasattr(User, key)
        pass

    def get_users(self, page_num=1, page_size=20, **kwargs):
        with switch_db(self.dao, self.DBMS):
            results = self.dao.list_by_page(page_num, page_size, **kwargs)
        return results
