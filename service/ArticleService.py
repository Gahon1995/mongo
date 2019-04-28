#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.Article import Article


class ArticleService(object):

    @staticmethod
    def del_article(aid):
        article = Article.get(aid=aid)
        if article is not None:
            article.delete()
            return True
        return False

    @staticmethod
    def articles_list(page_num=1, page_size=20, **kwargs):
        return Article.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    def get_an_article(**kwargs):
        return Article.get(**kwargs)

    @staticmethod
    def update(article):
        article.update()
