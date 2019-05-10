#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-11 00:27
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import redis

import Config

__redis = None


def get_redis(url='redis://@{0}:{1}/0'.format(Config.redis_host, Config.redis_port), new_con=False):
    global __redis
    if __redis is None or new_con:
        __redis = redis.from_url(url=url)
    return __redis


# class RedisClient(object):
#     _redis = None
#
#     def __init__(self, url='redis://@{0}:{1}/0'.format(Config.redis_host, Config.redis_port)):
#         RedisClient._redis = redis.from_url(url=url)
#
#     # 保证单例，减少连接数
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, '__instance'):
#             cls.__instance = object.__new__(cls)
#         return cls.__instance
#
#     @classmethod
#     def redis(cls):
#         if cls._redis is None:
#             raise BaseException("未初始化连接")
#         return cls._redis


if __name__ == '__main__':
    pass
