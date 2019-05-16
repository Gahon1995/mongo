#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-11 00:27
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import pickle

from redis import Redis as PyRedis
from Config import Config
from utils.func import singleton, available_value


@singleton
class Redis(PyRedis):
    # session = None

    def __init__(self, *args):
        args = {
            'host': Config.redis_host,
            'port': Config.redis_port,
            'db': 0,
            'password': Config.redis_password,
            'decode_responses': True
        }
        super().__init__(**args)

    def get(self, name, default=None):
        res = super().get(name)
        # if decode: res = res.decode()
        return res if res else default

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super().set(name, available_value(value), ex=ex, px=px, nx=nx, xx=xx)

    def set_dict(self, name, value):
        return self.set_pickle(name, value)
        # return self.set(name, json.dumps(value))

    def get_dict(self, name, default={}):
        return self.get_pickle(name, default)
        # res = self.get(name)
        # if res:
        #     return json.loads(res)
        # return default

    def set_pickle(self, name, value):
        return self.set(name, pickle.dumps(value, 0).decode())

    def get_pickle(self, name, default=None):
        res = self.get(name)
        return pickle.loads(res.encode()) if res else default

    # def smembers(self, name, default=[]):
    #     res = super().smembers(name)
    #     return [val.decode() for val in list(res)] if res else default


if __name__ == '__main__':
    pass
