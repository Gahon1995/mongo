#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:42
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from model.Article import Article


class ArticleService(object):

    @staticmethod
    def get_size(**kwargs):
        return Article.get_size(**kwargs)

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
        forbid = ("aid", "_id")
        article = Article.get(aid=aid)
        for key, value in condition.items():
            if key not in forbid and hasattr(article, key):
                setattr(article, key, value)
        return None

    @staticmethod
    def pretty_articles(articles: list):
        from prettytable import PrettyTable

        x = PrettyTable()

        if not isinstance(articles, list):
            articles = list(articles)
        field_names = ('aid', 'title', 'category', 'abstract', 'articleTags', 'authors', 'language', 'timestamp')
        x.field_names = field_names
        for article in articles:
            x.add_row(list(article[key] for key in field_names))

        print(x)
        pass


if __name__ == '__main__':
    from main import init

    init()
    _articles = ArticleService.articles_list()
