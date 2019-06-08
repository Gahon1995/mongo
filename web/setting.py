#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-08 15:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from flask import request

from service.user_service import UserService
from utils.func import get_best_dbms_by_region
from web.api.result import Result
from web.my_web import Web

session = Web().session
jwt = Web().jwt


@session.before_request
def cors():
    if request.method == 'OPTIONS':
        return


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = UserService().get_user_by_uid(identity['uid'], db_alias=get_best_dbms_by_region(identity['region']))
    return user


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return Result.gen_failed(404, msg=ret)
