#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 13:32
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from service.ArticleService import ArticleService
from utils.func import *


def article_manage(role='user', user=None):
    print("\n\n" + "=" * 20)
    print("1. 查询所有文章")
    print("2. 阅读指定文章")
    print("3. 查看热门文章")
    print("4. 创建新文章")
    print("5. 查看阅读历史")
    print("6. 删除指定文章")
    print("7. 更新文章信息")
    if role == 'admin':
        print("8. 更新热门文章")
    print("0. 返回上一级")
    print("=" * 20)

    mode = input("请选择操作: ")
    if mode == '1':
        articles_query_all()
        pass
    elif mode == '2':
        choices_article(user)
        pass
    elif mode == '3':
        show_popular()
        pass
    elif mode == '4':
        create_article(user)
        pass
    elif mode == '5':
        show_history(user)
        pass
    elif mode == '6':
        del_an_article(user, role)
        pass
    elif mode == '7':
        update_an_article(role, user)
        pass
    elif mode == '8':
        update_popular()
        pass
    elif mode == '0':
        return None
        pass
    else:
        pass

    article_manage(role, user)


def articles_query_all(page_num=1, page_size=20, **kwargs):
    total = ArticleService.get_size(**kwargs)

    articles = ArticleService.articles_list(page_num, page_size, **kwargs)

    ArticleService.pretty_articles(articles)
    show_next(page_num, page_size, total, articles_query_all)
    # total_pages = int(total / page_size)
    # flag = False
    # if total_pages > 1:
    #     flag = True
    # if flag:
    #     print("\n\t\t\t\t\t当前第{page_num}页， 总共{total_pages}页，共{total}条数据"
    #           .format(page_num=page_num,
    #                   total_pages=total_pages,
    #                   total=total))
    #
    # while flag:
    #     print("\t\t1. 上一页\t2. 下一页\t3. 指定页数\t4.返回上一级")
    #     mode = input("请选择操作： ")
    #     if mode == '1':
    #         if page_num <= 1:
    #             print("当前就在第一页哟")
    #         else:
    #             return articles_query_all(page_num - 1)
    #     elif mode == '2':
    #         if page_num >= total_pages:
    #             print("当前在最后一页哟")
    #         else:
    #             return articles_query_all(page_num + 1)
    #     elif mode == '3':
    #         num = int(input('请输入跳转页数: '))
    #         if 0 < num <= total_pages:
    #             return articles_query_all(num)
    #         else:
    #             print("输入页码错误")
    #     elif mode == '4':
    #         return None
    # input("\n\t按回车键返回")

    pass


def choices_article(user):
    aid = int(input("请输入要阅读的文章aid： "))
    article = ArticleService.get_an_article(aid=aid)
    if article is None:
        print("文章不存在")

    read_an_article(user, article)


def read_an_article(user, article):
    from service.ReadService import Read, ReadService
    import time

    time_read_start = time.time()
    print_an_article(article)

    # input("\n按回车返回")
    # TODO 阅读完后的操作，点赞、评论、分享等
    new_read = Read()
    new_read.aid = article
    new_read.uid = user
    while True:
        print("1. 点赞 \t2. 评论\t3. 分享\t4. 返回")
        mode = input("请选择操作: ")
        if mode == '1':
            new_read.agreeOrNot = 1
            print("点赞成功")
        elif mode == '2':
            new_read.commentOrNot = 1
            detail = input("请输入评论信息： ")
            new_read.commentDetail = detail
            print("评论成功")
        elif mode == '3':
            new_read.shareOrNot = 1
            print("分享成功")
        elif mode == '4':
            time_read_end = time.time()
            new_read.readTimeLength = time_read_end - time_read_start
            ReadService.save_new_read(new_read)
            return
        else:
            print("输入错入，请重新输入")

    pass


def print_an_article(article):
    print("\n" + "=" * 40)
    print("Title: {title:<13}   Aid: {aid:<8}  Category: {category:<10}"
          .format(title=article.title,
                  aid=article.aid,
                  category=article.category))
    print("Authors: {authors:<13} Tags: {tags:<8} Language: {language:<10}"
          .format(authors=article.authors,
                  tags=article.articleTags,
                  language=article.language))
    print("time: {0}".format(article.timestamp))
    print("abstract: {0}".format(article.abstract))
    print("=" * 15 + "content" + "=" * 15)
    print(article.text)
    print("\n" + "=" * 40)
    pass


def show_popular():
    # TODO 展示热门文章
    pass


def create_article(user):
    # TODO 创建新文章
    #       根据Article表的项内容创建文章，并且保存
    pass


def show_history(user):
    # TODO 展示历史阅读数据
    #       根据Read 表的数据展示当前用户的阅读历史
    pass


def del_an_article(user, role):
    aid = input("请输入要删除的文章aid： ")
    if role == 'user' and user is not None:
        article = ArticleService.get_an_article(aid=aid, authors=user.name)
        if article is None:
            print("您无权限删除该文章或者该文章不存在")
            return
        ArticleService.del_article(article)
    elif role == 'admin':
        ArticleService.del_by_aid(aid=aid)
    else:
        print("用户不存在或者权限错误")
        return

    print("删除成功")
    return None
    pass


def update_an_article(role, user):
    # TODO 管理员或者用户更新文章信息
    pass


def update_popular():
    pass


if __name__ == '__main__':
    from main import init

    init()
    # articles_query_all()
    # read_an_article(user)
    from service.UserService import UserService

    _user = UserService.get_an_user('admin')
