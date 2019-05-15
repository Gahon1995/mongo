#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:13
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.user import User
from db.mongodb import switch_mongo_db
from utils.consts import DBMS, Region
from utils.func import *
import logging

logger = logging.getLogger('userService')


class UserService(object):

    @staticmethod
    def hasattr(key):
        return hasattr(User, key)

    @staticmethod
    def get_uid(region):
        return UserService.__uid(db_alias=get_best_dbms_by_region(region))

    @staticmethod
    @switch_mongo_db(cls=User)
    def __uid(db_alias=None):
        check_alias(db_alias)
        return User.get_id('uid')

    @staticmethod
    def register(name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                 obtainedCredits: int):
        user = UserService.get_user_by_name(name)
        if user is not None:
            logger.info('用户名已存在')
            return False, '用户名已存在'
        re = False, ''

        uid = get_id_by_region(UserService.get_uid(region), region)
        for dbms in get_dbms_by_region(region):
            re = UserService.__register(uid, name, pwd, gender, email, phone, dept, grade, language, region, role,
                                        preferTags, obtainedCredits, db_alias=dbms)
            if not re[0]:
                break
        return re

    @staticmethod
    @switch_mongo_db(cls=User)
    def __register(uid, name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                   obtainedCredits: int, db_alias=None):

        check_alias(db_alias)

        user = User()
        user.uid = uid
        user.name = name
        user.pwd = pwd
        user.gender = gender
        user.email = email
        user.phone = phone
        user.dept = dept
        user.grade = grade
        user.language = language
        user.region = region
        user.role = role
        user.preferTags = preferTags
        user.obtainedCredits = obtainedCredits
        if user.save() is not None:
            logger.info('用户：{} 注册成功'.format(name))
            return True, '用户：{} 注册成功'.format(name)
        return False, '保存至数据库失败'

    @staticmethod
    @switch_mongo_db(cls=User)
    def users_list(page_num=1, page_size=20, db_alias=None, **kwargs):
        check_alias(db_alias)
        return User.list_by_page(page_num, page_size, **kwargs)

    @staticmethod
    @switch_mongo_db(cls=User)
    def count(db_alias=None, **kwargs):
        check_alias(db_alias)
        return User.count(**kwargs)

    @staticmethod
    def count_all(**kwargs):
        return UserService.count(db_alias=DBMS.DBMS1, **kwargs) + UserService.count(db_alias=DBMS.DBMS2, **kwargs)

    @staticmethod
    def get_user_by_name(name, db_alias=None):
        if db_alias is None:
            user = UserService.__get_user_by_name(name, db_alias=DBMS.DBMS1)
            if user is None:
                user = UserService.__get_user_by_name(name, db_alias=DBMS.DBMS2)
            return user
        else:
            return UserService.__get_user_by_name(name, db_alias=db_alias)

    @staticmethod
    @switch_mongo_db(cls=User)
    def __get_user_by_name(name, db_alias=None):
        check_alias(db_alias)
        return User.get(name=name)

    @staticmethod
    def get_user_by_uid(uid: int):
        return UserService.__get_user_by_uid(uid, db_alias=get_best_dbms_by_uid(uid))

    @staticmethod
    @switch_mongo_db(cls=User)
    def __get_user_by_uid(uid, db_alias=None):
        check_alias(db_alias)
        return User.get(uid=uid)

    @staticmethod
    def login(username, password):
        user = None
        for dbms in DBMS.all:
            user = UserService.__login(username, password, db_alias=dbms)
            if user is not None:
                break
        return user

    @staticmethod
    @switch_mongo_db(cls=User)
    def __login(username, password, db_alias=None):
        check_alias(db_alias)
        user = User.get(name=username)
        if user is not None and user.pwd == password:
            logger.info("用户 {} 登录成功".format(username))
            return user
        else:
            logger.info("用户名或者密码错误")
        return None

    @staticmethod
    def logout(name):
        logger.info('用户 {} 退出登录'.format(name))
        return True

    @staticmethod
    def update_by_uid(uid, **kwargs):
        user = UserService.get_user_by_uid(uid)
        if user is None:
            logger.info("uid:{}不存在".format(uid))
            return None

        # TODO 如何判断更新失败？（例如更新时网络异常）
        for dbms in get_dbms_by_uid(uid):
            user = UserService.update_user(user, db_alias=dbms, **kwargs)
            if user is None:
                break
        return user

    @staticmethod
    def update_by_name(name, **kwargs):
        user = UserService.get_user_by_name(name)
        if user is None:
            logger.info("name:{}不存在".format(name))
            return None

        # TODO 如何判断更新失败？（例如更新时网络异常）
        for dbms in get_dbms_by_uid(user.uid):
            user = UserService.update_user(user, db_alias=dbms, **kwargs)
            if user is None:
                break
        return user

    @staticmethod
    @switch_mongo_db(cls=User)
    def update_user(user, db_alias=None, **kwargs):
        check_alias(db_alias)
        forbid = ('name', 'id', '_id', 'region')
        if user is None:
            logger.info("用户不存在")
            return None

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return user.save()

    @staticmethod
    def del_user_by_name(name):
        user = UserService.get_user_by_name(name=name)
        if user is not None:
            for dbms in get_dbms_by_uid(user.uid):
                success = UserService.del_user(user, db_alias=dbms)
                if not success:
                    return False
        return True

    @staticmethod
    def del_user_by_uid(uid):
        user = UserService.get_user_by_uid(uid=uid)
        if user is not None:
            for dbms in get_dbms_by_uid(user.uid):
                success = UserService.del_user(user, db_alias=dbms)
                if not success:
                    return False
        return True

    @staticmethod
    @switch_mongo_db(cls=User)
    def del_user(user: User, db_alias=None):
        check_alias(db_alias)
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

        print(x)
    # ============================= 待调整     =======================

    # @staticmethod
    # @switch_mongo_db(cls=User)
    # def update_user_by_admin(user, db_alias=None):
    #     check_alias(db_alias)
    #     user.save()
    #     # TODO 如何判断更新失败？（例如更新时网络异常）
    #     return True

    # @staticmethod
    # @switch_mongo_db(cls=User)
    # def del_user_by_id(_id, db_alias=None):
    #     check_alias(db_alias)
    #     user = User.get(id=_id)
    #     if user is not None:
    #         user.delete()
    #         return True
    #     return False


if __name__ == '__main__':
    from main import init

    init()

    _users = UserService.users_list()
    UserService.pretty_users(_users)
