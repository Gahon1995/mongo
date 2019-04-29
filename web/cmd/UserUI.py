#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 13:32
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from service.UserService import UserService
from utils.func import show_next
import json


class UserUI(object):

    @staticmethod
    def login(username, password):
        return UserService.login(username, password)

    @staticmethod
    def user_query_all(page_num=1, page_size=20, **kwargs):
        total = UserService.get_size(**kwargs)
        # total_pages = int((total - 1) / page_size) + 1
        # print("\n" + "=" * 20)
        users = UserService.users_list(page_num, page_size, **kwargs)
        UserService.pretty_users(users)

        show_next(page_num=page_num, page_size=page_size, next_func=UserUI.user_query_all, total=total)

        # print("\n\t\t\t\t\t当前第{page_num}页， 总共{total_pages}页，共{total}条数据"
        #       .format(page_num=page_num,
        #               total_pages=total_pages,
        #               total=total))
        # flag = False
        # if total_pages > 1:
        #     flag = True
        #
        # while flag:
        #     print("\t\t1. 上一页\t2. 下一页\t3. 指定页数\t4.返回上一级")
        #     mode = input("请选择操作： ")
        #     if mode == '1':
        #         if page_num <= 1:
        #             print("当前就在第一页哟")
        #         else:
        #             return UserUI.user_query_all(page_num - 1)
        #     elif mode == '2':
        #         if page_num >= total_pages:
        #             print("当前在最后一页哟")
        #         else:
        #             return UserUI.user_query_all(page_num + 1)
        #     elif mode == '3':
        #         num = int(input('请输入跳转页数: '))
        #         if 0 < num <= total_pages:
        #             return UserUI.user_query_all(num)
        #         else:
        #             print("输入页码错误")
        #     elif mode == '4':
        #         return None
        # input("\n\t按回车键返回")

    @staticmethod
    def user_query_by_name():
        name = input("\n请输入查询的用户名: ")
        user = UserService.get_an_user(name)
        if user is None:
            print("用户名不存在")
        else:
            UserService.pretty_users([user])
            input("按回车键返回")
        return None

    @staticmethod
    def user_query_by_condition(**kwargs):
        condition = input("\n请输入json格式的查询条件: ")

        try:
            con = json.loads(condition)
            for key, value in con.items():
                if UserService.hasattr(key):
                    kwargs[key] = value
                else:
                    print("输入的JSON字段错误，请检查。")
                    return None
            return UserUI.user_query_all(**kwargs)
        except json.JSONDecodeError:
            print("输入格式错误")
            return None

    @staticmethod
    def update_user_info(**kwargs):
        username = input("请输入要更新的用户名：")
        user = UserService.get_an_user(username)
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

    @staticmethod
    def del_user():
        username = input("请输入要删除的用户名： ")
        user = UserService.get_an_user(username)
        if user is None:
            print("该用户不存在")
            return None
        UserService.pretty_users([user])
        choice = input("是否删除该用户？（Y or N）： ")
        if choice == 'Y' or choice == 'y' or choice == 'yes':
            UserService.del_user(user)
            print("删除成功")

        return None

    @staticmethod
    def add_user():
        # TODO 管理员添加用户
        pass

    @staticmethod
    def user_manage():
        print("\n" + "=" * 20)
        print("1. 查询所有用户\n2. 根据用户名查询\n3. 根据条件查询\n4. 更改用户信息\n5. 添加用户\n6. 删除用户\n7. 返回上一级")
        print("=" * 20)
        mode = input("请选择操作：  ")
        if mode == '1':
            UserUI.user_query_all()
        elif mode == '2':
            UserUI.user_query_by_name()
        elif mode == '3':
            UserUI.user_query_by_condition()
        elif mode == '4':
            UserUI.update_user_info()
        elif mode == '5':
            UserUI.add_user()
        elif mode == '6':
            UserUI.del_user()
        elif mode == '7':
            return None
        else:
            print("输入错误")
        UserUI.user_manage()
