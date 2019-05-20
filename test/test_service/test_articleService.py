#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-10 21:12
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from test.test_base import TestBase
from service.article_service import ArticleService
from config import DBMS


class TestBaseArticleService(TestBase):

    def test_get_id(self):
        ids = ArticleService().get_id()
        print(ids)

    def test_count(self):
        dbms1 = ArticleService().count(db_alias=DBMS.DBMS1)
        print("count dbms1: {}".format(dbms1))

        dbms2 = ArticleService().count(db_alias=DBMS.DBMS2)
        print("count dbms1: {}".format(dbms2))

    def test_search_by_title(self):
        articles = ArticleService().get_articles_by_title('title6')
        ArticleService().pretty_articles(articles)

    def test_get_articles_by_category(self):
        articles = ArticleService().get_articles_by_category('science')
        ArticleService().pretty_articles(articles)

    def test_add_an_article(self):
        re = ArticleService().add_an_article('test', 'gahon', 'science', 'asdf', 'asdfas', 'asdf', 'asdf')
        assert re
        re = ArticleService().add_an_article('test', 'gahon', 'technology', 'asdf', 'asdfas', 'asdf', 'asdf')
        assert re
        articles = ArticleService().get_articles_by_title('test', db_alias=DBMS.DBMS1)
        ArticleService().pretty_articles(articles)

        articles = ArticleService().get_articles_by_title('test', db_alias=DBMS.DBMS2)
        ArticleService().pretty_articles(articles)

    def test_del_article(self):
        # re = ArticleService().del_by_aid(308)
        # assert re
        #
        # article = ArticleService().get_an_article_by_id(308)
        # assert article is None

        re = ArticleService().add_an_article('test_article', 'gahon', 'science', 'asdf', 'asdfas', 'asdf', 'asdf')
        assert re
        articles = ArticleService().get_articles_by_title('test_article')
        ArticleService().pretty_articles(articles)
        _id = articles[0].id
        re = ArticleService().del_article(articles[0])
        assert re
        article = ArticleService().get_an_article_by_id(_id)
        assert article is None

    def test_articles_list(self):
        articles = ArticleService().get_articles(db_alias=DBMS.DBMS2)
        ArticleService.pretty_articles(articles)

    def test_get_by_aid(self):
        article = ArticleService().get_articles_by_title('title5')[0]
        article1 = ArticleService().get_an_article_by_id(article.id)
        ArticleService.pretty_articles([article])
        assert article1 is not None and article.title == article1.title

    def test_update_article_by_id(self):
        a = ArticleService().get_articles_by_title('title5')[0]
        article = ArticleService().get_an_article_by_id(a.id)
        ArticleService.pretty_articles([article])

        ArticleService().update_an_article(article, {"title": "update24", "language": 'zh'})

        article = ArticleService().get_an_article_by_id(a.id)
        ArticleService.pretty_articles([article])
        assert article.language == 'zh'
