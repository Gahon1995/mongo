#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 17:37
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

import logging


class Config(object):
    # logging 配置
    debug_level = logging.DEBUG
    log_in_file = False
    log_file_name = './mongo.log'

    #  MongoDB 相关配置
    mongo_db_name = 'mongo-new'
    mongo_host = 'gahon.xyz'  # 服务器
    # mongo_host = '127.0.0.1'  # 宿舍
    # mongo_host = '192.168.109.130'    # 工位
    mongo_port = 27017

    # bj mongo 配置
    # bj_mongo_host = '10.211.55.5'
    bj_mongo_host = '127.0.0.1'
    bj_mongo_port = 27017

    # hk mongo 配置
    hk_mongo_host = '127.0.0.1'
    # hk_mongo_host = 'gahon.xyz'
    hk_mongo_port = 27018

    # Redis 配置
    redis_host = '127.0.0.1'
    redis_port = 6379

    DBMS = {
        'DBMS1': {
            # 'name': 'beijing',
            'host': '127.0.0.1',
            'port': 27017,
        },
        'DBMS2': {
            # 'name': 'hongkong',
            'host': '127.0.0.1',
            'port': 27018,
        },
    }

    rules = {
        'User': {
            'field': 'region',
            'location': {
                'Beijing': ['DBMS1'],
                'Hong Kong': ['DBMS2'],
            }
        },
        'Article': {
            'field': 'category',
            'location': {
                'science': ['DBMS1', 'DBMS2'],
                'technology': ['DBMS2']
            }
        },

    }
