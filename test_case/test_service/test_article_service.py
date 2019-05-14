#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-10 21:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from test_case.base_test import TestBase
from service.article_service import ArticleService, Article
from utils.consts import Region


class TestBaseArticleService(TestBase):

    def test_get_size(self):
        size = ArticleService.count(db_alias=Region.bj)

        print('bj: size: ' + str(size))
        size = ArticleService.count(db_alias=Region.hk)

        print('hk: size: ' + str(size))

    def test_search_by_title(self):
        articles = ArticleService.search_by_title('title3', db_alias=Region.bj)
        assert articles is not None
        print(articles)

    def test_connection(self):
        res = ArticleService.get_an_article(title='title57')
        print(res)
