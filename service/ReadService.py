#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.Read import Read


class ReadService(object):

    @staticmethod
    def save_new_read(new_read):
        new_read.save()

    @staticmethod
    def reads_list(page_num=1, page_size=20, **kwargs):
        return Read.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    def del_read(_id):
        article = Read.get(id=_id)
        if article is not None:
            article.delete()
            return True
        return False

    @staticmethod
    def read_info(_id):
        return Read.get(id=_id)
