#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.article import Article
from db.mongodb import switch_mongo_db
from utils.consts import DBMS, Category
from utils.func import check_alias, get_dbms_by_category
from datetime import datetime
import logging

logger = logging.getLogger('ArticleService')


class ArticleService(object):

    @staticmethod
    def get_id():
        return max(ArticleService.__id(DBMS.DBMS1), ArticleService.__id(DBMS.DBMS2))

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def __id(db_alias=None):
        check_alias(db_alias)
        return Article.get_id('aid')

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def count(db_alias=DBMS.DBMS2, **kwargs):
        check_alias(db_alias)
        return Article.count(**kwargs)

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def search_by_title(title, db_alias=DBMS.DBMS2) -> list:
        """
            因为DBMS2上存有所有的文章，所以默认直接在DBMS2上搜索就行
            # TODO 测试该方法是否有用
        :param title:
        :param db_alias:
        :return: list, 里边存的article
        """
        check_alias(db_alias)
        return Article.objects(title__contains=title)

    @staticmethod
    def add_an_article(title, authors, category, abstract, articleTags, language, text, image=None,
                       video=None):
        article = Article()
        article.title = title
        article.authors = authors
        article.category = category
        article.abstract = abstract
        article.articleTags = articleTags
        article.language = language
        article.text = text
        article.image = image
        article.video = video
        article.update_time = datetime.utcnow()

        _id = ArticleService.get_id()
        if category == Category.science:
            article.aid = _id if _id % 2 == 0 else _id + 1
        if category == Category.technology:
            article.aid = _id if _id % 2 == 1 else _id + 1

        for dbms in get_dbms_by_category(article.category):
            ArticleService.save_article(article, db_alias=dbms)
            article.id = None
        pass

    @staticmethod
    @switch_mongo_db(cls=Article)
    def save_article(article, db_alias=None):
        check_alias(db_alias)
        if article.save() is not None:
            logger.info('文章"{}"保存成功'.format(article.title))

    @staticmethod
    @switch_mongo_db(cls=Article)
    def del_by_id(_id, db_alias=None, **kwargs):
        check_alias(db_alias)
        article = Article.get(id=_id, **kwargs)
        ArticleService.del_article(article, db_alias=db_alias)

    @staticmethod
    @switch_mongo_db(cls=Article)
    def del_article(article, db_alias=None):
        check_alias(db_alias)
        if article is not None:
            article.delete()
        return True

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def articles_list(page_num=1, page_size=20, db_alias=DBMS.DBMS2, **kwargs):
        check_alias(db_alias)
        return Article.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def get_an_article(db_alias=DBMS.DBMS2, **kwargs):
        check_alias(db_alias)
        return Article.objects(**kwargs).first()

    @staticmethod
    @switch_mongo_db(cls=Article)
    def get_an_article_by_id(_id, db_alias=None):
        check_alias(db_alias)
        return Article.objects(id=_id).first()

    @staticmethod
    def update_an_article(article, condition: dict):
        forbid = ("id", "_id", 'update_time', 'aid')
        for key, value in condition.items():
            if key not in forbid and hasattr(article, key):
                setattr(article, key, value)
        article.update_time = datetime.utcnow()
        for dbms in get_dbms_by_category(article.category):
            ArticleService.save_article(article, db_alias=dbms)

    @staticmethod
    @switch_mongo_db(cls=Article, default_db=DBMS.DBMS2)
    def update_by_id(_id, condition, db_alias=DBMS.DBMS2):
        check_alias(db_alias)
        article = Article.objects(id=_id).first()
        ArticleService.update_an_article(article, condition)

    @staticmethod
    def pretty_articles(articles: list):
        from prettytable import PrettyTable
        from datetime import datetime

        x = PrettyTable()

        if not isinstance(articles, list):
            articles = list(articles)
        field_names = (
            'id', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'create_time', 'update_time')
        x.field_names = field_names
        for article in articles:
            # 需要对时间进行时区转换
            x.add_row(list(article.__getattribute__(key).astimezone()
                           if isinstance(article.__getattribute__(key), datetime)
                           else article.__getattribute__(key)
                           for key in field_names
                           ))

        print(x)
        pass


if __name__ == '__main__':
    from main import init

    init()
    _articles = ArticleService.articles_list()
