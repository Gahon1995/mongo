#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 13:32
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from service.article_service import ArticleService
from service.read_service import ReadService
from service.popular_service import PopularService
from utils.func import *

from prettytable import PrettyTable


def article_manage(role='user', user=None):
    print("\n\n" + "=" * 20)
    print("1. 查询所有文章")
    print("2. 阅读指定文章")
    print("3. 查看热门文章")
    print("4. 创建新文章")
    print('5. 查看我创建的文章')
    print("6. 查看阅读历史")
    print("7. 删除指定文章")
    print("8. 更新文章信息")
    if role == 'admin':
        print("9. 更新热门文章")
        print("10. 查看所有阅读历史")
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
        show_my_article(user)
        pass
    elif mode == '6':
        history(user)
        pass
    elif mode == '6':
        del_an_article(user, role)
        pass
    elif mode == '8':
        update_an_article(role, user)
        pass
    elif mode == '9':
        update_popular()
        pass
    elif mode == '10':
        history_admin()
        pass
    elif mode == '0':
        return None
        pass
    else:
        pass

    article_manage(role, user)


def articles_query_all(**kwargs):
    total = ArticleService.get_size(**kwargs)
    query_all(total, **kwargs)


def query_all(total, page_num=1, page_size=20, **kwargs):
    articles = ArticleService.articles_list(page_num, page_size, **kwargs)

    ArticleService.pretty_articles(articles)
    show_next(page_num, page_size, total, query_all, **kwargs)

    pass


def choices_article(user):
    # TODO 文章数量过多时分页显示
    from prettytable import PrettyTable
    keyword = input("请输入要阅读的文章部分标题： ")
    if keyword == '':
        return
    articles = ArticleService.search_by_title(keyword)
    if len(articles) == 0:
        print("未找到相关文章")
        return

    x = PrettyTable()
    x.field_names = ("num", "title", "authors", "abstract")
    for index, article in enumerate(articles):
        x.add_row([index, article.title, article.authors, article.abstract])
    print(x)
    while True:
        try:
            index = int(input("请选择要阅读的序号（ -1 退出）： "))
        except ValueError:
            print("输入错误")
            return
        if 0 <= index < len(articles):
            read_an_article(user, articles[index])
            break
        elif index == -1:
            break
        else:
            print("输入错误，请重新输入")


def read_an_article(user, article):
    from service.read_service import Read, ReadService
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
    print("\n" + "=" * 50)
    print("Title: {title:<13}  Category: {category:<10}"
          .format(title=article.title,
                  category=article.category))
    print("Authors: {authors:<13} Tags: {tags:<8} Language: {language:<10}"
          .format(authors=article.authors,
                  tags=article.articleTags,
                  language=article.language))
    print("time: {0}".format(article.update_time.astimezone()))
    print("abstract: {0}".format(article.abstract))
    print("=" * 22 + "content" + "=" * 22)
    print(article.text)
    print("\n" + "=" * 50)
    pass


def show_popular():
    # TODO 展示热门文章
    print('=' * 30)
    print('1. 今日热门文章')
    print('2. 最近一周热门文章')
    print('3. 最近一个月热门文章')
    print('4. 返回上一级')
    print('=' * 30)

    mode = input("请选择操作：")
    if mode == '1':
        show_daily_popular()
        pass
    elif mode == '2':
        show_weekly_popular()
        pass
    elif mode == '3':
        show_monthly_popular()
        pass
    elif mode == '4':
        return
    else:
        pass
    show_popular()


def show_daily_popular():
    rank = PopularService.get_daily_rank(datetime.today())
    show_rank(rank)
    pass


def show_weekly_popular():
    rank = PopularService.get_weekly_rank(datetime.today())
    show_rank(rank)
    pass


def show_monthly_popular():
    rank = PopularService.get_monthly_rank(datetime.today())
    show_rank(rank)
    pass


def show_rank(rank):
    if rank is None:
        print("当前并无数据，请联系管理员生成")
        return
    x = PrettyTable()
    x.field_names = ('index', 'title', 'id')
    print("\nlast update time: {}".format(rank.update_time))
    for index, article in enumerate(rank.articleAidList):
        x.add_row((index, article.title, article.id))
    print(x)
    input("\n按回车键返回")


def create_article(user):
    # TODO 输入内容为空判断
    #       根据Article表的项内容创建文章，并且保存
    title = input("请输入title: ")
    while title == '':
        title = input("输入不能为空，请重新输入: ")
    category = input("请输入category: ")
    abstract = input("请输入abstract: ")
    articleTags = input("请输入articleTags: ")
    language = input("请输入language: ")
    text = input("请输入text: ")
    image = input("请输入image: ")
    video = input("请输入video: ")
    ArticleService.add_an_article(title, user.name, category, abstract, articleTags, language, text, image, video)
    pass


from prettytable import PrettyTable

x = PrettyTable()


def history(user):
    total = ReadService.get_size(uid=user)
    show_history(user, total)


def show_history(user, total, page_num=1, page_size=20, **kwargs):
    # TODO 数据量大时分页显示
    x.clear()
    x.field_names = ('index', 'title', 'readTimeLength', 'readSequence',
                     'agreeOrNot', 'commentOrNot', 'shareOrNot', 'commentDetail', 'readTime')
    # TODO 展示历史阅读数据
    #       根据Read 表的数据展示当前用户的阅读历史
    reads = ReadService.get_history(user, page_num, page_size)
    for index, read in enumerate(reads):
        x.add_row((index, read.aid.title, read.readTimeLength, read.readSequence,
                   read.agreeOrNot, read.commentOrNot, read.shareOrNot, read.commentDetail, read.create_time))

    print(x)
    show_next(page_num, page_size, total, show_history, **kwargs)
    # input("按回车键返回")
    pass


def history_admin():
    total = ReadService.get_size()
    show_history_admin(total)


def show_history_admin(total, page_num=1, page_size=20, **kwargs):
    # TODO 数据量大时分页显示
    # x.clear()
    x.clear_rows()
    x.field_names = ('index', 'title', 'user', 'readTimeLength', 'readSequence',
                     'agreeOrNot', 'commentOrNot', 'shareOrNot', 'commentDetail', 'readTime')
    # TODO 展示历史阅读数据
    #       根据Read 表的数据展示当前用户的阅读历史
    reads = ReadService.reads_list(page_num, page_size)
    for index, read in enumerate(reads):
        x.add_row((index, read.aid.title, read.uid.name, read.readTimeLength, read.readSequence,
                   read.agreeOrNot, read.commentOrNot, read.shareOrNot, read.commentDetail, read.create_time))

    print(x)
    show_next(page_num, page_size, total, show_history_admin, **kwargs)
    # input("按回车键返回")
    pass


def del_an_article(user, role):
    aid = input("请输入要删除的文章aid： ")
    if aid == '':
        return
    if role == 'user' and user is not None:
        article = ArticleService.get_an_article(id=aid, authors=user.name)
        if article is None:
            print("您无权限删除该文章或者该文章不存在")
            return
        ArticleService.del_article(article)
    elif role == 'admin':
        ArticleService.del_by_id(_id=aid)
    else:
        print("用户不存在或者权限错误")
        return

    print("删除成功")
    return None
    pass


def update_an_article(role, user):
    # TODO 管理员或者用户更新文章信息
    aid = input("请输入要更新的文章的id：")
    if aid is None or aid == '':
        print("无输入，返回上一级")
        return
    try:
        article = ArticleService.get_an_article(id=aid)
    except Exception:
        print("id不存在")
        return
    if article is None:
        print("文章不存在。")
        return
    if (role == 'user' and article.authors == user.name) or role == 'admin':
        print_an_article(article)
        update_info = input("请输入要更改的信息（json格式：）")
        if update_info == '':
            return
        try:
            con = json.loads(update_info)
            if ArticleService.update_an_article(article, con):
                print("更新成功")
        except json.JSONDecodeError:
            print("输入不是json格式")
            return None
    else:
        print("无权限对该文章进行操作")

    pass


def update_popular():
    print("更新今日热门")
    PopularService.update_daily_rank()
    print("更新一周热门")
    PopularService.update_monthly_rank()
    print("更新一月热门")
    PopularService.update_weekly_rank()
    print("更新完成")
    pass


def show_my_article(user):
    articles = ArticleService.articles_list(authors=user.name)
    ArticleService.pretty_articles(articles)

    input("按回车返回")
    return


if __name__ == '__main__':
    from main import init

    init()
    # articles_query_all()
    # read_an_article(user)
    from service.user_service import UserService

    _user = UserService.get_an_user('admin')
    choices_article(_user)
