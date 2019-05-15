#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 15:38
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.user import User
from dao.base_dao import BaseDB
from utils.func import singleton


@singleton
class UserDao(BaseDB):

    def __init__(self):
        super().__init__(User)

    pass
