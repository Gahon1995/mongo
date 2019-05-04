#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.Article import Article
import logging

logger = logging.getLogger('ArticleService')


class ArticleService(object):

    @staticmethod
    def get_size(**kwargs):
        return Article.count(**kwargs)

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
    def del_by_aid(aid, **kwargs):
        article = Article.get(aid=aid, **kwargs)
        if article is not None:
            article.delete()
            return True
        return False

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
    def update_an_article(article):
        article.update()

    @staticmethod
    def update_by_condition(aid, condition):
        from datetime import datetime
        forbid = ("aid", "_id", 'update_time')
        article = Article.get(aid=aid)
        for key, value in condition.items():
            if key not in forbid and hasattr(article, key):
                setattr(article, key, value)
        article.update_time = datetime.utcnow()
        article.save()
        return True

    @staticmethod
    def pretty_articles(articles: list):
        from prettytable import PrettyTable

        x = PrettyTable()

        if not isinstance(articles, list):
            articles = list(articles)
        field_names = (
            'aid', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'create_time', 'update_time')
        x.field_names = field_names
        for article in articles:
            x.add_row(list(article.__getattribute__(key) for key in field_names))

        print(x)
        pass


if __name__ == '__main__':
    from main import init

    init()
    _articles = ArticleService.articles_list()
