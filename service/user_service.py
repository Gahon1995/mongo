#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:13
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from model.user import User
from db.mongodb import switch_mongo_db
from utils.func import *
import logging

logger = logging.getLogger('userService')


@singleton
class UserService(object):

    @staticmethod
    def hasattr(key):
        """
            判断User中是否有key这个属性
        :param key:  待判断的属性
        :return: True or False
        """
        return hasattr(User, key)

    def get_uid(self, region):
        """
            通过region来获取当前region所对应的数据库的下一个id应该是啥
        :param region: 地区，该参数需要和consts 类中Region所对应的值相等
        :return:
        """
        return self.__uid(db_alias=get_best_dbms_by_region(region))

    @switch_mongo_db(cls=User)
    def __uid(self, db_alias=None):
        check_alias(db_alias)
        return User.get_id('uid')

    def register(self, name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                 obtainedCredits, timestamp=None):
        """
            用户注册，返回注册结果和信息
        :param timestamp:
        :param name:  用户名
        :param pwd:     密码
        :param gender:  性别
        :param email:
        :param phone:
        :param dept:
        :param grade:
        :param language:
        :param region: 地区，该值应与Region类中的值一样
        :param role:
        :param preferTags:
        :param obtainedCredits:
        :return: list[True or False, msg]
        """
        user = self.get_user_by_name(name)
        if user is not None:
            logger.info('用户名已存在')
            return False, '用户名已存在'
        re = False, ''

        uid = get_uid_by_region(self.get_uid(region), region)
        for dbms in get_dbms_by_region(region):
            re = self.__register(uid, name, pwd, gender, email, phone, dept, grade, language, region, role,
                                 preferTags, obtainedCredits, timestamp, db_alias=dbms)
            if not re[0]:
                break
        return re

    @switch_mongo_db(cls=User)
    def __register(self, uid, name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                   obtainedCredits: int, timestamp=None, db_alias=None):

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
        user.timestamp = timestamp or datetime.datetime.utcnow()
        if user.save() is not None:
            logger.info('用户：{} 注册成功'.format(name))
            return True, '用户：{} 注册成功'.format(name)
        return False, '保存至数据库失败'

    @switch_mongo_db(cls=User)
    def users_list(self, page_num=1, page_size=20, db_alias=None, **kwargs) -> list:
        """
            获取db_alias 所对应的数据库里边的用户列表，采用分页
            可以通过**kwargs进行高级查询，
        :param page_num:    查询页码
        :param page_size:   每页的数据量大小
        :param db_alias:    数据库的别名
        :param kwargs:      其他的一些查询参数
        :return:
        """
        check_alias(db_alias)
        return User.list_by_page(page_num, page_size, **kwargs)

    @switch_mongo_db(cls=User)
    def count(self, db_alias=None, **kwargs):
        """
            计算db_alias所对应的的数据库下满足条件的用户数量
        :param db_alias:
        :param kwargs:  查询参数字典， 为空则统计所有用户数量
        :return:
        """
        check_alias(db_alias)
        return User.count(**kwargs)

    def count_all(self, **kwargs):
        """
            统计所有数据库中的用户总量
        :param kwargs:  制定特殊查询参数
        :return:
        """
        count = 0
        for dbms in DBMS.all:
            count += self.count(db_alias=dbms, **kwargs)
        return count

    def get_user_by_name(self, name: str, db_alias: str = None) -> User:
        """
            通过用户名进行查询
        :param name:    查询的用户名
        :param db_alias:    查找的数据库名称， 如果为空的话则查询所有数据库
        :return:
        """
        user = None
        if db_alias is None:
            for dbms in DBMS.all:
                user = self.__get_user_by_name(name, db_alias=dbms)
                if user is not None:
                    break
            return user
        else:
            return self.__get_user_by_name(name, db_alias=db_alias)

    @switch_mongo_db(cls=User)
    def __get_user_by_name(self, name, db_alias=None):
        check_alias(db_alias)
        return User.get(name=name)

    def get_user_by_uid(self, uid: int) -> User:
        """
            根据uid进行用户查询
        :param uid:
        :return:
        """
        return self.__get_user_by_uid(uid, db_alias=get_best_dbms_by_uid(uid))

    @switch_mongo_db(cls=User)
    def __get_user_by_uid(self, uid, db_alias=None):
        check_alias(db_alias)
        return User.get(uid=uid)

    def login(self, username, password) -> User:
        """
            用户登录
        :param username:
        :param password:
        :return: User实体，登录失败返回None
        """
        user = None
        for dbms in DBMS.all:
            user = self.__login(username, password, db_alias=dbms)
            if user is not None:
                break
        return user

    @switch_mongo_db(cls=User)
    def __login(self, username, password, db_alias=None):
        check_alias(db_alias)
        user = User.get(name=username, pwd=password)
        if user is not None:
            logger.info("用户 {} 登录成功".format(username))
            return user
        else:
            logger.info("用户名或者密码错误")
        return None

    def logout(self, name):
        logger.info('用户 {} 退出登录'.format(name))
        return True

    def update_by_uid(self, uid, **kwargs) -> object:
        """
            根据uid进行更新用户数据
        :param uid:
        :param kwargs:      待更新的数据
        :return:    user or None
        """
        user = self.get_user_by_uid(uid)
        if user is None:
            logger.info("uid:{}不存在".format(uid))
            return None

        # TODO 如何判断更新失败？（例如更新时网络异常）
        for dbms in get_dbms_by_uid(uid):
            user = self.update_user(user, db_alias=dbms, **kwargs)
            if user is None:
                break
        return user

    def update_by_name(self, name, **kwargs):
        """
            根据name进行更新
        :param name:
        :param kwargs:  更新的数据
        :return:
        """
        user = self.get_user_by_name(name)
        if user is None:
            logger.info("name:{}不存在".format(name))
            return None

        # TODO 如何判断更新失败？（例如更新时网络异常）
        for dbms in get_dbms_by_uid(user.uid):
            user = self.update_user(user, db_alias=dbms, **kwargs)
            if user is None:
                break
        return user

    @switch_mongo_db(cls=User)
    def update_user(self, user: User, db_alias=None, **kwargs):
        """
            根据user实例进行更新用户数据
        :param user:    待更新的用户数据
        :param db_alias:
        :param kwargs:      更新的字段和对应的值
        :return:
        """
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

    def del_user_by_name(self, name):

        user = self.get_user_by_name(name=name)
        if user is not None:
            for dbms in get_dbms_by_uid(user.uid):
                success = self.del_user(user, db_alias=dbms)
                if not success:
                    return False
        return True

    def del_user_by_uid(self, uid):
        user = self.get_user_by_uid(uid=uid)
        if user is not None:
            for dbms in get_dbms_by_uid(user.uid):
                success = self.del_user(user, db_alias=dbms)
                if not success:
                    return False
        return True

    @switch_mongo_db(cls=User)
    def del_user(self, user: User, db_alias=None):
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

    _users = UserService().users_list()
    UserService().pretty_users(_users)
