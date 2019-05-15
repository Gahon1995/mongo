#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 14:31
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

import functools
import json
import pytz
from datetime import datetime, date

from mongoengine.base import BaseDocument

from utils.consts import Region, Category, DBMS

from Config import Config


def singleton(cls):
    """
    将一个类作为单例
    来自 https://wiki.python.org/moin/PythonDecoratorLibrary#Singleton
    """

    cls.__new_original__ = cls.__new__

    @functools.wraps(cls.__new__)
    def singleton_new(cls, *args, **kw):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it

        cls.__it__ = it = cls.__new_original__(cls, *args, **kw)
        it.__init_original__(*args, **kw)
        return it

    cls.__new__ = singleton_new
    cls.__init_original__ = cls.__init__
    cls.__init__ = object.__init__

    return cls


tz = pytz.timezone("Asia/Shanghai")


def utc_2_local(t):
    return t.astimezone()


# 使json能够转化datetime对象
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return utc_2_local(obj).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# 将 MongoDB 的 document转化为json形式
def convert_mongo_2_json(o):
    def convert(dic_data):
        # 对于引用的Id和该条数据的Id，这里都是ObjectId类型的
        from bson import ObjectId
        # 字典遍历
        for key, value in dic_data.items():
            # 如果是列表，则递归将值清洗
            if isinstance(value, list):
                for index, l in enumerate(value):
                    if isinstance(l, ObjectId):
                        value[index] = str(l)
                    elif isinstance(l, dict):
                        convert(l)
            else:
                if isinstance(value, ObjectId):
                    dic_data[key] = str(dic_data.get(key))
        return dic_data

    ret = {}
    # 判断其是否为Document
    if isinstance(o, BaseDocument):
        """
        转化为son形式，son的说明，摘自官方
        SON data.
        A subclass of dict that maintains ordering of keys and provides a
        few extra niceties for dealing with SON. SON provides an API
        similar to collections.OrderedDict from Python 2.7+.
        """
        data = o.to_mongo()
        # 转化为字典
        data = data.to_dict()
        ret = convert(data)
    # 将数据转化为json格式， 因json不能直接处理datetime类型的数据，故需要区分处理
    ret = json.dumps(ret, cls=DateEncoder)
    return ret


def show_next(page_num, page_size, total, next_func, db_alias=None, **kwargs):
    total_pages = int((total - 1) / page_size) + 1
    flag = False

    print("\n\t\t\t\t\t当前第{page_num}页， 总共{total_pages}页，共{total}条数据"
          .format(page_num=page_num,
                  total_pages=total_pages,
                  total=total))
    if total_pages > 1:
        flag = True
    while flag:
        print("\t\t1. 上一页\t2. 下一页\t3. 指定页数\t4.返回上一级")
        mode = input("请选择操作： ")
        if mode == '1':
            if page_num <= 1:
                print("当前就在第一页哟")
            else:
                return next_func(total=total, page_num=page_num - 1, db_alias=db_alias, **kwargs)
        elif mode == '2':
            if page_num >= total_pages:
                print("当前在最后一页哟")
            else:
                return next_func(total=total, page_num=page_num + 1, db_alias=db_alias, **kwargs)
        elif mode == '3':
            num = int(input('请输入跳转页数: '))
            if 0 < num <= total_pages:
                return next_func(total=total, page_num=num, db_alias=db_alias, **kwargs)
            else:
                print("输入页码错误")
        elif mode == '4':
            return None
    input("\n\t按回车键返回")
    pass


def merge_dict_and_sort(dict_1, dict_2) -> list:
    for key, value in dict_2.items():
        if dict_1.get(key) is None:
            dict_1.setdefault(key, value)
        else:
            dict_1[key] += value

    return sorted(dict_1.items(), key=lambda item: item[1], reverse=True)


def sort_dict(data) -> list:
    return sorted(data.items(), key=lambda item: item[1], reverse=True)


# 工具类简单，如果是字节，转成str
def bytes_to_str(s, encoding='utf-8'):
    """Returns a str if a bytes object is given."""
    if isinstance(s, bytes):
        return s.decode(encoding)
    return s


class AliasIsNoneException(Exception):
    pass


class DbmsErrorException(Exception):
    pass


def check_alias(db_alias):
    if db_alias is None:
        raise AliasIsNoneException("alias is None")
    if not (db_alias == DBMS.DBMS1 or db_alias == DBMS.DBMS2):
        raise DbmsErrorException("alias is wrong, please check")


def get_dbms_by_region(region):
    if region == Region.bj:
        return DBMS.DBMS1
    else:
        return DBMS.DBMS2


def get_dbms_by_category(category):
    if category == Category.science:
        return [DBMS.DBMS1, DBMS.DBMS2]
    else:
        return [DBMS.DBMS2]


def get_start_end_object_id():
    pass


def get_dbms_location(model: str, value: str):
    return Config.rules[model]['location'][value]


def get_dbms_field(model: str):
    return Config.rules[model]['field']
