#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-15 15:40
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from mongoengine import DoesNotExist
import logging

logger = logging.getLogger('db')


class BaseDB(object):

    def __init__(self, model):
        self.model = model

    def list_by_page(self, page_num=1, page_size=20, **kwargs):
        """
            分页数据查询

        :param page_num: 查询的页码，默认第一页
        :param page_size: 每一页显示的数量
        :param kwargs: 查询的条件
        :return: 符合条件的分页数后据
        """
        offset = (page_num - 1) * page_size
        return self.model.objects(**kwargs).skip(offset).limit(page_size)

    def count(self, **kwargs):
        """

        :return: 当前数据的总量
        """
        return self.model.objects(**kwargs).count()

    def find(self, **kwargs):
        """
            查询所有数据（未分页）
        :param kwargs: 查询条件
        :return:
        """
        return self.model.objects(**kwargs)

    def find_one(self, **kwargs):
        """
        返回符合条件的所有值的第一个

        :param kwargs: 查询条件
        :return:
        """
        return self.model.objects(**kwargs).first()

    def get(self, **kwargs):
        """
        获取一个unique的项

        :param kwargs: 查询条件
        :return:
        """
        try:
            user = self.model.objects(**kwargs).get()
            return user
        except DoesNotExist:
            return None

    def delete_by(self, **kwargs):
        """
            删除符合条件的数据
        :param kwargs:
        :return:
        """
        return self.model.objects(**kwargs).delete()

    def get_id(self, _id: str):
        """
            查询当前最大的id

        :param _id: 当前class 的id 名称
        :return:
        """

        obj = self.model.objects.order_by('-' + _id).limit(1).first()
        if obj is None:
            return 1
        else:
            return int(obj.__getattribute__(_id)) + 1

    @staticmethod
    def save_model(model):
        model.save()
