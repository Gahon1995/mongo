#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:13
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.User import User
import logging

logger = logging.getLogger('userService')


class UserService(object):

    @staticmethod
    def hasattr(key):
        return hasattr(User, key)

    @staticmethod
    def users_list(page_num=1, page_size=20, **kwargs):
        return User.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    def get_size(**kwargs):
        return User.get_size(**kwargs)

    @staticmethod
    def get_an_user(name):
        return User.get(name=name)

    @staticmethod
    def login(name, password):
        user = User.get(name=name)
        if user is not None and user.pwd == password:
            logger.debug("用户 {} 登录成功".format(name))
            return user
        else:
            logger.debug("用户名或者密码错误")
        return None

    @staticmethod
    def logout(name):
        logger.debug('用户 {} 退出登录'.format(name))
        return True

    @staticmethod
    def register(name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                 obtainedCredits: int):
        user = User.get(name=name)
        if user is not None:
            logger.debug('用户名已存在')
            return False

        user = User(name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                    obtainedCredits)
        if user.save() is not None:
            return True
        return False

    @staticmethod
    def update(name, **kwargs):
        forbid = ('name', 'uid', '_id')
        user = User.get(name=name)
        if user is None:
            logger.debug("用户名不存在")
            return False

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])
        user.save()

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    def update_user(user, **kwargs):
        forbid = ('name', 'uid', '_id')
        if user is None:
            logger.debug("用户名不存在")
            return False

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])
        user.save()

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    def update_by_admin(name, **kwargs):
        forbid = ('name', 'uid', '_id')
        user = User.get(name=name)
        if user is None:
            logger.debug("用户名不存在")
            return False

        # TODO 添加管理员能够更改用户名的功能
        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])

        user.save()
        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    def del_user_by_name(name):
        user = User.get(name=name)
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    def del_user(user: User):
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    def del_user_by_uid(uid):
        user = User.get(uid=uid)
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    def pretty_users(users):
        from prettytable import PrettyTable

        x = PrettyTable()
        field_names = ['uid', 'name', 'pwd', 'gender', 'email', 'phone', 'dept', 'grade',
                       'language', 'region', 'role', 'preferTags', 'obtainedCredits', 'timestamp']
        x.field_names = field_names
        for user in users:
            x.add_row(list(user[key] for key in field_names))

            # data = json.loads(user.__str__())
            # data.pop('_id')
            # x.add_row(data.values())

        print(x)


if __name__ == '__main__':
    from main import init

    init()

    users = UserService.users_list()
    UserService.pretty_users(users)
