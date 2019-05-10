#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-10 21:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from test_case.base_test import TestBase
from service.article_service import ArticleService


class TestBaseArticleService(TestBase):

    def test_get_size(self):
        size = ArticleService.get_size()

        print('size: ' + str(size))

    def test_search_by_title(self):
        articles = ArticleService.search_by_title('title3')
        assert articles is not None
        print(articles)
