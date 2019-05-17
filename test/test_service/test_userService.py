#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-14 13:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from test.test_base import TestBase
from service.user_service import UserService
from config import DBMS


class TestUserService(TestBase):

    def test_user_list(self):
        users = UserService().users_list(db_alias=DBMS.DBMS1)
        UserService().pretty_users(users)

        print('total: {}'.format(len(users)))

        users = UserService().users_list(db_alias=DBMS.DBMS2)
        UserService().pretty_users(users)

        print('total: {}'.format(len(users)))

    def test_register(self):
        re1 = UserService().register('gahon', 'password', 'male', 'asdf', 'asdfasdf', 'asdf', 'asdf', 'asdf',
                                     'Beijing', 'asdf', 'asdfas', '123')

        assert re1
        print(re1)

    def test_count(self):
        print()
        cnt = UserService().count(db_alias=DBMS.DBMS1)
        print('DBMS1:', cnt)
        cnt = UserService().count(db_alias=DBMS.DBMS2)
        print('DBMS2:', cnt)
        cnt = UserService().count_all()
        print('all: ', cnt)

    def test_get_user_by_name(self):
        user = UserService().get_user_by_name('user4')
        assert user is not None
        print(user)

        admin = UserService().get_user_by_name('admin', db_alias=DBMS.DBMS1)
        assert admin is not None

        admin = UserService().get_user_by_name('admin', db_alias=DBMS.DBMS2)
        assert admin is None
        print(admin)

    def test_get_by_uid(self):
        user = UserService().get_user_by_uid(34)
        # assert user is not None
        print(user)
        user = UserService().get_user_by_uid(23)
        # assert user is not None
        print(user)

    def test_login(self):
        user = UserService().login('admin', 'admin')
        assert user is not None
        print(user)

        user = UserService().login('gahon', 'password')
        assert user is not None
        print(user)

        user = UserService().login('admin', 'qweqwe')
        assert user is None

    def test_update(self):
        user = UserService().update_by_uid(1, gender='female', email='ewrqwr')
        assert user is not None
        print(user)

        user = UserService().update_by_name('user56', gender='female', email='awerasfsa')
        assert user is not None
        print(user)

    def test_del(self):
        # UserService().del_user_by_uid(49)
        # user = UserService().get_user_by_uid(49)
        # assert user is None

        UserService().del_user_by_name('gahon')
        user = UserService().get_user_by_name('gahon')
        assert user is None
