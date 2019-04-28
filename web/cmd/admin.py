#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 23:31
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import json
from service.UserService import UserService


def login_by_admin():
    print("输入 'return' 返回上一级")

    username = input("请输入用户名：")
    if username == 'return':
        return 1

    password = input("请输入密 码： ")
    if password == 'return':
        return 1

    if username == 'admin' and UserService.login(username, password):
        return admin_manage()
    else:
        print("用户名或密码错误，请重新输入")
        login_by_admin()
    return None


def admin_manage():
    print("\n" + "=" * 20)
    print("当前登录用户： admin\n")
    print("1. 用户管理\n2. 文章管理\n3. 热门管理\n4. 退出登录")
    print("=" * 20)
    mode = input("请选择操作:  ")
    if mode == '1':
        user_manage()
    elif mode == '2':
        article_manage()
    elif mode == '3':
        popular_manage()
    elif mode == '4':
        return None
    else:
        print("输入错误。。。")
    admin_manage()


def user_manage():
    print("\n" + "=" * 20)
    print("1. 查询所有用户\n2. 根据用户名查询\n3. 根据条件查询\n4. 更改用户信息\n5. 删除用户\n6. 返回上一级")
    print("=" * 20)
    mode = input("请选择操作：  ")
    if mode == '1':
        user_query_all()
    elif mode == '2':
        user_query_by_name()
    elif mode == '3':
        user_query_by_condition()
    elif mode == '4':
        update_user_info()
    elif mode == '5':
        pass
    elif mode == '6':
        return None
    else:
        print("输入错误")
    user_manage()


def user_query_all(page_num=1, page_size=20, **kwargs):
    total = UserService.get_size(**kwargs)
    total_pages = int(total / page_size) + 1
    # print("\n" + "=" * 20)
    users = UserService.users_list(page_num, page_size, **kwargs)
    UserService.pretty_users(users)
    flag = False
    if total_pages > 1:
        flag = True
    if flag:
        print("\n\t\t\t\t\t当前第{page_num}页， 总共{total_pages}页，共{total}条数据"
              .format(page_num=page_num,
                      total_pages=total_pages,
                      total=total))

    while flag:
        print("\t\t1. 上一页\t2. 下一页\t3. 指定页数\t4.返回上一级")
        mode = input("请选择操作： ")
        if mode == '1':
            if page_num <= 1:
                print("当前就在第一页哟")
            else:
                return user_query_all(page_num - 1)
        elif mode == '2':
            if page_num >= total_pages:
                print("当前在最后一页哟")
            else:
                return user_query_all(page_num + 1)
        elif mode == '3':
            num = int(input('请输入跳转页数: '))
            if 0 < num <= total_pages:
                return user_query_all(num)
            else:
                print("输入页码错误")
        elif mode == '4':
            flag = False
    input("\n\t按回车键返回")


def user_query_by_name():
    name = input("\n请输入查询的用户名: ")
    return user_query_all(name=name)


def user_query_by_condition(**kwargs):
    condition = input("\n请输入json格式的查询条件: ")

    try:
        con = json.loads(condition)
        for key, value in con.items():
            kwargs[key] = value
        return user_query_all(**kwargs)
    except json.JSONDecodeError:
        print("输入格式错误")
        return None


def update_user_info(**kwargs):
    username = input("请输入要更新的用户名：")
    user = UserService.user_info(username)
    if user is None:
        print("用户不存在")
    UserService.pretty_users([user])
    update_date = input("请输入修改的内容(json格式)： ")
    try:
        con = json.loads(update_date)
        for key, value in con.items():
            kwargs[key] = value
        return UserService.update_by_admin(username, **kwargs)
    except json.JSONDecodeError:
        print("输入不是json格式")
        return None


def article_manage():
    pass


def popular_manage():
    pass


if __name__ == '__main__':
    from main import init

    init()
    user_manage()
    # user_query_by_name()
