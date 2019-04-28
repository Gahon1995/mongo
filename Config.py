#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 17:37
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

import logging

# logging 配置
debug_level = logging.DEBUG
log_in_file = False
log_file_name = './mongo.log'

#  MongoDB 相关配置
mongo_db_name = 'mongo-test'
mongo_host = 'gahon.xyz'
mongo_port = 27017