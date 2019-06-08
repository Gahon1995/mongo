#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-02 23:37
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import logging

from config import DBMS, Config
from db.redis_db import Redis
from utils.func import singleton, check_alias


@singleton
class RedisService(object):

    def __init__(self):
        self.redis = dict()
        self.log = logging.getLogger('RedisService')
        self.debug = Config().REDIS_DEBUG
        for dbms in DBMS().all:
            self.redis[dbms] = self._gen_redis(dbms)

    def get_redis(self, dbms) -> Redis:
        check_alias(dbms)
        return self.redis[dbms]

    def _gen_redis(self, dbms):
        # print(DBMS().redis[dbms]['host'])
        # host = DBMS().redis[dbms]['host'],
        # port = DBMS().redis[dbms]['port'],
        # db = 0,
        # password = DBMS().redis[dbms]['redis_password'],
        # decode_responses = True
        args = DBMS().redis[dbms]
        return Redis(**args)

    def reset_redis(self):
        if self.debug:
            self.log.debug(f'reset redis keys')
        for dbms, redis in self.redis.items():
            redis.delete_by_pattern('*')

    def set_dict(self, dbms, key, value):
        if self.debug:
            self.log.debug(f'set to {dbms}, key: {key}')
        return self.get_redis(dbms).set_dict(key, value)

    def get_dict(self, dbms, key):
        data = self.get_redis(dbms).get_dict(key)

        if self.debug and data != {}:
            self.log.debug(f'get from {dbms}, key: {key}')
        return data

    def delete_key(self, dbms, key):
        if self.debug:
            self.log.debug(f'delete key from {dbms}, key: {key}')

        return self.get_redis(dbms).delete(key)

    def delete_key_by_pattern(self, dbms, pattern):
        if self.debug:
            self.log.debug(f'delete key from {dbms}, pattern: {pattern}')

        return self.get_redis(dbms).delete_by_pattern(pattern)

    def set_dict_to_all(self, key, value):
        if self.debug:
            self.log.debug(f'set to all dbms, key: {key}')
        res = True
        for dbms, redis in self.redis.items():
            res = redis.set_dict(key, value)
        return res

    def get_dict_from_all(self, key):
        data = {}
        for dbms, redis in self.redis.items():
            data = redis.get_dict(key)
            if data != {}:
                break
        if self.debug and data != {}:
            self.log.debug(f'get from all dbms, key: {key}')
        return data

    def delete_key_to_all(self, key):
        if self.debug:
            self.log.debug(f'delete key to all, key: {key}')
        del_num = 0
        for dbms, redis in self.redis.items():
            del_num += redis.delete(key)
        return del_num

    def delete_key_by_pattern_to_all(self, pattern):
        if self.debug:
            self.log.debug(f'delete key to all, pattern: {pattern}')
        del_num = 0
        for dbms, redis in self.redis.items():
            del_num += redis.delete_by_pattern(pattern)
        return del_num
