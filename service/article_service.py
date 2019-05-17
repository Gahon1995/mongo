#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.article import Article
from db.mongodb import switch_mongo_db
from service.ids_service import IdsService

from utils.func import *
import logging
from config import DBMS


@singleton
class ArticleService(object):
    field_names = ['aid', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'timestamp',
                   'update_time']

    def __init__(self):
        self.logger = logging.getLogger('ArticleService')

    @staticmethod
    def get_id():
        # _id = -1
        # for dbms in DBMS.all:
        #     _id = max(self.__id(dbms), _id)
        # return _id
        return IdsService().next_id('aid')

    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def __id(self, db_alias=None):
        check_alias(db_alias)
        return Article.get_id('aid')

    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def count(self, db_alias=DBMS.DBMS2, **kwargs):
        check_alias(db_alias)
        return Article.count(**kwargs)

    def get_articles_by_title(self, title, db_alias=None) -> list:
        """
            根据文章标题进行搜索
            # TODO 测试该方法是否有用
        :param db_alias:
        :param title:
        :return: list, 里边存的article
        """
        articles = list()  # 保存所有数据库上的不同文章

        aids = list()  # 保存在查询过程中已经出现过的文章

        if db_alias is None:
            for dbms in DBMS.all:
                tmp_articles = self.__search_by_title(title, db_alias=dbms)
                for article in tmp_articles:
                    # 判断是否已经在其他DBMS中出现过了
                    if article.aid not in aids:
                        articles.append(article)
                        aids.append(article.aid)
        else:
            articles = self.__search_by_title(title, db_alias=db_alias)
        return articles

    @switch_mongo_db(cls=Article)
    def __search_by_title(self, title, db_alias=None) -> list:
        """
            因为DBMS2上存有所有的文章，所以默认直接在DBMS2上搜索就行
            # TODO 测试该方法是否有用
        :param title:
        :param db_alias:
        :return: list, 里边存的article
        """
        check_alias(db_alias)
        return Article.objects(title__contains=title)

    def add_an_article(self, title, authors, category, abstract, articleTags, language, text, image=None,
                       video=None, timestamp=None):
        aid = get_id_by_category(self.get_id(), category)
        for dbms in get_dbms_by_category(category):
            self.__add_an_article(aid, title, authors, category, abstract, articleTags, language, text, image,
                                  video, timestamp, db_alias=dbms)
        IdsService().set_id('aid', aid)
        return True

    @switch_mongo_db(cls=Article)
    def __add_an_article(self, aid, title, authors, category, abstract, articleTags, language, text, image=None,
                         video=None, timestamp=None, db_alias=None):

        check_alias(db_alias)
        article = Article()
        article.aid = aid
        article.title = title
        article.authors = authors
        article.category = category
        article.abstract = abstract
        article.articleTags = articleTags
        article.language = language
        article.text = text
        article.image = image
        article.video = video
        article.update_time = datetime.datetime.utcnow()
        article.timestamp = timestamp or get_timestamp()

        return self.save_article(article)

    def save_article(self, article):
        if article.save() is not None:
            self.logger.info('文章"{}"保存成功'.format(article.title))
            return True
        return False

    def del_by_aid(self, aid, **kwargs):
        re = None
        for dbms in get_dbms_by_aid(aid):
            re = self.__del_by_id(aid, db_alias=dbms, **kwargs)
            pass
        return re

    @switch_mongo_db(cls=Article)
    def __del_by_id(self, aid, db_alias=None, **kwargs):
        check_alias(db_alias)

        re = Article.objects(aid=aid, **kwargs).delete()
        return re

    def del_article(self, article):
        if article is not None:
            for dbms in get_dbms_by_category(article.category):
                self.__del_by_id(article.aid, db_alias=dbms)
        return True

    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def get_articles(self, page_num=1, page_size=20, db_alias=None, **kwargs):
        # TODO 去掉默认db设置，在所有数据库中，根据数量进行分页以及返回相关数据
        # check_alias(db_alias)
        return Article.list_by_page(page_num, page_size, **kwargs)

    # @staticmethod
    # @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    # def get_an_article(db_alias=DBMS.DBMS2, **kwargs):
    #     check_alias(db_alias)
    #     return Article.objects(**kwargs).first()

    def get_article_by_aid(self, aid):
        # TODO 修改实现方法
        article = None
        for dbms in get_dbms_by_aid(aid):
            article = self.__get_an_article_by_aid(aid, db_alias=dbms)
            if article is not None:
                break
        return article

    @switch_mongo_db(cls=Article)
    def __get_an_article_by_aid(self, aid, db_alias=None):
        check_alias(db_alias)
        return Article.objects(aid=aid).first()

    def update_an_article(self, aid, condition: dict):
        """
            根据aid更新文章

        :param aid:
        :param condition:  Json格式更新内容
        :return:
        """
        for dbms in get_dbms_by_aid(aid):
            self.__update_article(aid, condition, db_alias=dbms)

    @switch_mongo_db(cls=Article)
    def __update_article(self, aid, condition: dict, db_alias=None):
        check_alias(db_alias)
        article = self.__get_an_article_by_aid(aid, db_alias=db_alias)
        if article is None:
            return

        forbid = ("id", "_id", 'update_time', 'aid')
        for key, value in condition.items():
            if key not in forbid and hasattr(article, key):
                setattr(article, key, value)
        article.update_time = datetime.datetime.utcnow()
        article.save()

    # =============== 已测试 ===============

    @staticmethod
    def pretty_articles(articles: list):
        pretty_models(articles, ArticleService.field_names)


if __name__ == '__main__':
    from main import init

    init()
    _articles = ArticleService.get_articles()
