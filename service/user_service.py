#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:13
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.user import User
from db.mongodb import switch_mongo_db
import logging

logger = logging.getLogger('userService')


class UserService(object):

    @staticmethod
    def hasattr(key):
        return hasattr(User, key)

    @staticmethod
    @switch_mongo_db(cls=User)
    def users_list(page_num=1, page_size=20, db_alias=None, **kwargs):
        return User.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    @switch_mongo_db(cls=User)
    def count(db_alias=None, **kwargs):
        return User.count(**kwargs)

    @staticmethod
    @switch_mongo_db(cls=User)
    def get_an_user(name, db_alias=None):
        return User.get(name=name)

    @staticmethod
    @switch_mongo_db(cls=User)
    def login(username, password, db_alias=None):
        if username is None or password is None:
            return None
        user = User.get(name=username)
        if user is not None and user.pwd == password:
            logger.info("用户 {} 登录成功".format(username))
            return user
        else:
            logger.info("用户名或者密码错误")
        return None

    @staticmethod
    @switch_mongo_db(cls=User)
    def logout(name, db_alias=None):
        logger.info('用户 {} 退出登录'.format(name))
        return True

    @staticmethod
    @switch_mongo_db(cls=User)
    def register(name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                 obtainedCredits: int, db_alias=None):
        user = User.get(name=name)
        if user is not None:
            logger.info('用户名已存在')
            return False

        user = User(name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                    obtainedCredits)
        if user.save() is not None:
            logger.info('用户：{} 注册成功'.format(name))
            return True
        return False

    @staticmethod
    @switch_mongo_db(cls=User)
    def update(name, db_alias=None, **kwargs):
        forbid = ('name', 'uid', '_id')
        user = User.get(name=name)
        if user is None:
            logger.info("用户{}不存在".format(name))
            return False

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])
        user.save()

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    @switch_mongo_db(cls=User)
    def update_user(user, db_alias=None, **kwargs):
        forbid = ('name', 'uid', '_id')
        if user is None:
            logger.info("用户名不存在")
            return False

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])
        user.save()

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    @switch_mongo_db(cls=User)
    def update_by_admin(name, db_alias=None, **kwargs):
        forbid = ('name', 'uid', '_id')
        user = User.get(name=name)
        if user is None:
            logger.info("用户名不存在")
            return False

        # TODO 添加管理员能够更改用户名的功能
        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])

        user.save()
        # TODO 如何判断更新失败？（例如更新时网络异常）
        return True

    @staticmethod
    @switch_mongo_db(cls=User)
    def del_user_by_name(name, db_alias=None):
        user = User.get(name=name)
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    @switch_mongo_db(cls=User)
    def del_user(user: User, db_alias=None):
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    @switch_mongo_db(cls=User)
    def del_user_by_uid(uid, db_alias=None):
        user = User.get(id=uid)
        if user is not None:
            user.delete()
            return True
        return False

    @staticmethod
    def pretty_users(users):
        from prettytable import PrettyTable

        x = PrettyTable()
        field_names = ['id', 'name', 'pwd', 'gender', 'email', 'phone', 'dept', 'grade',
                       'language', 'region', 'role', 'preferTags', 'obtainedCredits', 'create_time']
        x.field_names = field_names
        for user in users:
            x.add_row(list(user.__getattribute__(key) for key in field_names))

            # data = json.loads(user.__str__())
            # data.pop('_id')
            # x.add_row(data.values())

        print(x)


if __name__ == '__main__':
    from main import init

    init()

    users = UserService.users_list()
    UserService.pretty_users(users)
