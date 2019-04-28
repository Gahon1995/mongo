#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 23:32
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from service.UserService import UserService


def login_by_user():
    print("输入 'return' 返回上一级")

    username = input("请输入用户名：")
    if username == 'return':
        return 1

    password = input("请输入密 码： ")
    if password == 'return':
        return 1

    if UserService.login(username, password):
        print("登录成功。。。\n\n\n")
        return user_manage(username)
    else:
        print("用户名或密码错误，请重新输入")
        login_by_user()


def user_manage(username):
    print("=" * 20)
    print("登录用户： {}\n\n".format(username))
    print("1. 用户管理\n2. 文章管理\n3. 热门管理\n4. 退出登录\n")
    print("=" * 20)
    mode = input("请选择操作:  ")
