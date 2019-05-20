#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import logging

from bson import ObjectId

from model.article import Article
from service.ids_service import IdsService
from utils.func import *


@singleton
class ArticleService(object):
    field_names = ['aid', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'timestamp',
                   'update_time']

    def __init__(self):
        self.logger = logging.getLogger('ArticleService')

    @staticmethod
    def get_model(dbms: str):
        class Model(Article):
            meta = {
                'db_alias': dbms,
                'collection': 'article'
            }
            pass

        return Model

    @staticmethod
    def get_id():

        return IdsService().next_id('aid')

    def has_article(self, aid, db_alias):
        return self.count(aid=aid, db_alias=db_alias)

    def count(self, db_alias=None, **kwargs):
        check_alias(db_alias)
        return self.get_model(db_alias).count(**kwargs)

    def get_articles_by_title(self, title, db_alias=None) -> list:
        """
            根据文章标题进行搜索
            # TODO 测试该方法是否有用
        :param db_alias:
        :param title:
        :return: list, 里边存的article
        """
        articles = list()  # 保存所有数据库上的不同文章

        titles = list()  # 保存在查询过程中已经出现过的文章

        if db_alias is None:
            for dbms in DBMS.all:
                tmp_articles = self.__search_by_title(title, db_alias=dbms)
                for article in tmp_articles:
                    # 判断是否已经在其他DBMS中出现过了
                    if article.title not in titles:
                        articles.append(article)
                        titles.append(article.title)
        else:
            articles = self.__search_by_title(title, db_alias=db_alias)
        return articles

    def __search_by_title(self, title, db_alias=None) -> list:
        """
            因为DBMS2上存有所有的文章，所以默认直接在DBMS2上搜索就行
            # TODO 测试该方法是否有用
        :param title:
        :param db_alias:
        :return: list, 里边存的article
        """
        check_alias(db_alias)
        return self.get_model(db_alias).objects(title__contains=title)

    def get_articles_by_category(self, category, db_alias=None) -> list:
        """
            根据文章标题进行搜索
            # TODO 测试该方法是否有用
        :param db_alias:
        :param category:
        :return: list, 里边存的article
        """
        articles = list()  # 保存所有数据库上的不同文章

        titles = list()  # 保存在查询过程中已经出现过的文章

        if db_alias is None:
            for dbms in DBMS.all:
                tmp_articles = self.__search_by_category(category, db_alias=dbms)
                for article in tmp_articles:
                    # 判断是否已经在其他DBMS中出现过了
                    if article.title not in titles:
                        articles.append(article)
                        titles.append(article.title)
        else:
            articles = self.__search_by_category(category, db_alias=db_alias)
        return articles

    def __search_by_category(self, category, db_alias=None) -> list:
        """
            因为DBMS2上存有所有的文章，所以默认直接在DBMS2上搜索就行
            # TODO 测试该方法是否有用
        :param category:
        :param db_alias:
        :return: list, 里边存的article
        """
        check_alias(db_alias)
        return self.get_model(db_alias).objects(category=category)

    def add_an_article(self, title, authors, category, abstract, articleTags, language, text, image=None,
                       video=None, timestamp=None):
        aid = self.get_id()
        for dbms in get_dbms_by_category(category):
            self.__add_an_article(aid, title, authors, category, abstract, articleTags, language, text, image,
                                  video, timestamp, db_alias=dbms)
            self.init_be_read_for_article(aid, db_alias=dbms)
        return True

    def __add_an_article(self, aid, title, authors, category, abstract, articleTags, language, text, image=None,
                         video=None, timestamp=None, db_alias=None):

        check_alias(db_alias)
        article = self.get_model(db_alias)()
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

    def init_be_read_for_article(self, aid, db_alias=None, timestamp=None):
        from service.be_read_service import BeReadService

        check_alias(db_alias=db_alias)

        be_read = BeReadService().get_model(db_alias)()
        be_read.aid = aid
        be_read.bid = BeReadService().get_bid()
        be_read.timestamp = timestamp or get_timestamp()
        be_read.save()

    def save_article(self, article):
        if article.save() is not None:
            self.logger.info('文章"{}"保存成功'.format(article.title))
            return True
        return False

    def del_by_filed(self, field, value, **kwargs):
        re = None
        for dbms in DBMS.all:
            re = self.__del_by_filed(field, value, db_alias=dbms, **kwargs)
            pass
        return re

    def __del_by_filed(self, field, value, db_alias=None, **kwargs):
        check_alias(db_alias)
        kwargs[field] = value
        re = self.get_model(db_alias).objects(**kwargs).delete()
        return re

    def del_by_aid(self, aid, **kwargs):
        re = self.del_by_filed('aid', aid, **kwargs)

        return re

    def del_article(self, article):
        if article is not None:
            for dbms in get_dbms_by_category(article.category):
                self.__del_by_filed('aid', article.aid, db_alias=dbms)
        return True

    def get_articles(self, page_num=1, page_size=20, db_alias=None, **kwargs):
        # TODO 去掉默认db设置，在所有数据库中，根据数量进行分页以及返回相关数据
        check_alias(db_alias)
        return self.get_model(db_alias).list_by_page(page_num, page_size, **kwargs)

    def get_an_article_by_id(self, _id):
        # TODO 修改实现方法
        article = None
        for dbms in DBMS.all:
            article = self.__get_an_article_by_id(_id, db_alias=dbms)
            if article is not None:
                break
        return article

    def __get_an_article_by_id(self, _id, db_alias=None):
        check_alias(db_alias)
        if not isinstance(_id, ObjectId):
            _id = ObjectId(_id)
        return self.get_model(db_alias).objects(id=_id).first()

    def get_an_article_by_aid(self, aid):
        # TODO 修改实现方法
        article = None
        for dbms in DBMS.all:
            article = self.__get_an_article_by_aid(aid, db_alias=dbms)
            if article is not None:
                break
        return article

    def __get_an_article_by_aid(self, aid, db_alias=None):
        check_alias(db_alias)

        return self.get_model(db_alias).objects(aid=aid).first()

    def update_an_article(self, article, condition: dict):
        """
            根据aid更新文章

        :param article:
        :param condition:  Json格式更新内容
        :return:
        """
        for dbms in get_dbms_by_category(article.category):
            self.__update_article(article, condition, db_alias=dbms)

    def __update_article(self, article, condition: dict, db_alias=None):
        check_alias(db_alias)
        article = self.__get_an_article_by_id(article.id, db_alias=db_alias)
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
