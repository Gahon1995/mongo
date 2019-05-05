#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.article import Article
import logging

logger = logging.getLogger('ArticleService')


class ArticleService(object):

    @staticmethod
    def get_size(**kwargs):
        return Article.count(**kwargs)

    @staticmethod
    def search_by_title(name):
        # TODO 测试该方法是否有用
        return Article.objects(title__contains=name)

    @staticmethod
    def add_an_article(title, authors, category, abstract, articleTags, language, text, image=None, video=None):
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

        if article.save() is not None:
            logger.info('文章"{}"保存成功'.format(title))

        pass

    @staticmethod
    def del_by_id(_id, **kwargs):
        article = Article.get(id=_id, **kwargs)
        if article is not None:
            article.delete()
            # return True
        return True

    @staticmethod
    def del_article(article):
        article.delete()

    @staticmethod
    def articles_list(page_num=1, page_size=20, **kwargs):
        return Article.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    def get_an_article(**kwargs):
        return Article.get(**kwargs)

    @staticmethod
    def update_an_article(article, condition: dict):
        from datetime import datetime
        forbid = ("id", "_id", 'update_time')
        for key, value in condition.items():
            if key not in forbid and hasattr(article, key):
                setattr(article, key, value)
        article.update_time = datetime.utcnow()
        article.save()
        return True

    @staticmethod
    def update_by_id(_id, condition):
        article = Article.get(id=_id)
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
