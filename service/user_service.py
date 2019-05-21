#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:13
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import logging

from bson import ObjectId

from model.user import User
from service.ids_service import IdsService
from utils.func import *

logger = logging.getLogger('userService')


@singleton
class UserService(object):
    field_names = ['uid', 'name', 'pwd', 'gender', 'email', 'phone', 'dept', 'grade',
                   'language', 'region', 'role', 'preferTags', 'obtainedCredits', 'create_time']

    def __init__(self):
        self.user = User

    @staticmethod
    def get_model(dbms):
        class Users(User):
            meta = {
                'db_alias': dbms,
                'collection': 'user'
            }
            pass

        return Users

    @staticmethod
    def hasattr(key):
        """
            判断User中是否有key这个属性
        :param key:  待判断的属性
        :return: True or False
        """
        return hasattr(User, key)

    @staticmethod
    def get_uid():
        """
            通过region来获取当前region所对应的数据库的下一个id应该是啥
        # :param region: 地区，该参数需要和consts 类中Region所对应的值相等
        :return:
        """
        return IdsService().next_id('uid')

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

        uid = self.get_uid()
        for dbms in get_dbms_by_region(region):
            re = self.__register(uid, name, pwd, gender, email, phone, dept, grade, language, region, role,
                                 preferTags, obtainedCredits, timestamp, db_alias=dbms)
            if not re[0]:
                break
        return re

    def __register(self, uid, name, pwd, gender, email, phone, dept, grade, language, region, role, preferTags,
                   obtainedCredits: int, timestamp=None, db_alias=None):

        check_alias(db_alias)

        user = self.get_model(db_alias)()
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
        user.timestamp = timestamp or get_timestamp()
        re = user.save()
        if re is not None:
            logger.info('用户：{} 注册成功'.format(name))
            return True, '用户：{} 注册成功'.format(name)
        return False, '保存至数据库失败'

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
        return self.get_model(db_alias).list_by_page(page_num, page_size, **kwargs)

    def count(self, db_alias=None, **kwargs):
        """
            计算db_alias所对应的的数据库下满足条件的用户数量
        :param db_alias:
        :param kwargs:  查询参数字典， 为空则统计所有用户数量
        :return:
        """
        check_alias(db_alias)
        return self.get_model(db_alias).count(**kwargs)

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
                user = self.get_user_by_name(name, db_alias=dbms)
                if user is not None:
                    break
            return user
        else:
            check_alias(db_alias)
            return self.get_model(db_alias).get(name=name)

    def get_user_by_id(self, _id, db_alias=None) -> User:
        """
            根据id进行用户查询
        :param db_alias:
        :param _id:
        :return:
        """
        if db_alias is None:
            user = None
            for dbms in DBMS.all:
                user = self.get_user_by_id(_id=_id, db_alias=dbms)
                if user is not None:
                    break
            return user
        else:
            check_alias(db_alias)
            if not isinstance(_id, ObjectId):
                _id = ObjectId(_id)
            return self.get_model(db_alias).get(id=_id)

    def get_user_by_uid(self, uid, db_alias=None) -> User:
        """
            根据id进行用户查询
        :param db_alias:
        :param uid:
        :return:
        """
        if db_alias is None:
            user = None
            for dbms in DBMS.all:
                user = self.get_user_by_uid(uid=uid, db_alias=dbms)
                if user is not None:
                    break
            return user
        else:
            check_alias(db_alias)
            return self.get_model(db_alias).get(uid=uid)

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

    def __login(self, username, password, db_alias=None):
        check_alias(db_alias)
        user = self.get_model(db_alias).get(name=username, pwd=password)
        if user is not None:
            logger.info("用户 {} 登录成功".format(username))
            return user
        else:
            logger.info("用户名或者密码错误")
        return None

    def logout(self, name):
        logger.info('用户 {} 退出登录'.format(name))
        return True

    def update_by_id(self, _id, db_alias=None, **kwargs):
        """
            根据name进行更新
        :param db_alias:
        :param _id:
        :param kwargs:  更新的数据
        :return:
        """
        user = self.get_user_by_id(_id, db_alias=db_alias)
        if user is None:
            if db_alias is None:
                logger.info("_id:{}不存在".format(_id))
            else:
                logger.info("数据不同步， DBMS: {}中找不到{}的信息".format(db_alias, _id))
            return None
        if db_alias is None:
            # TODO 如何判断更新失败？（例如更新时网络异常）
            for dbms in get_dbms_by_region(user.region):
                user = self.update_by_id(_id, db_alias=dbms, **kwargs)
                # if user is None:
                #     break
            return user
        else:
            check_alias(db_alias)
            return self.update_user(user, **kwargs)

    def update_by_name(self, name, db_alias=None, **kwargs):
        """
            根据name进行更新
        :param db_alias:
        :param name:
        :param kwargs:  更新的数据
        :return:
        """
        user = self.get_user_by_name(name, db_alias=db_alias)
        if user is None:
            if db_alias is None:
                logger.info("name:{}不存在".format(name))
            else:
                logger.info("数据不同步， DBMS: {}中找不到{}的信息".format(db_alias, name))
            return None
        if db_alias is None:

            # TODO 如何判断更新失败？（例如更新时网络异常）
            for dbms in get_dbms_by_region(user.region):
                user = self.update_by_name(name, db_alias=dbms, **kwargs)
                if user is None:
                    break
            return user
        else:
            check_alias(db_alias)
            return self.update_user(user, **kwargs)

    def update_user(self, user: User, **kwargs):
        """
            根据user实例进行更新用户数据
        :param user:    待更新的用户数据
        # :param db_alias:
        :param kwargs:      更新的字段和对应的值
        :return:
        """
        forbid = ('name', 'id', 'uid', 'region')
        if user is None:
            logger.info("用户不存在")
            return None

        for key in kwargs:
            if key not in forbid and hasattr(user, key):
                setattr(user, key, kwargs[key])

        # TODO 如何判断更新失败？（例如更新时网络异常）
        return user.save()

    def del_user_by_name(self, name, db_alias=None):

        user = self.get_user_by_name(name=name, db_alias=db_alias)

        if user is not None:
            if db_alias is None:
                for dbms in get_dbms_by_region(user.region):
                    self.del_user_by_name(name, db_alias=dbms)
                    # if not success:
                    #     return False
                return True
            else:
                return user.delete()
        return False

    def del_user_by_id(self, _id, db_alias=None):
        user = self.get_user_by_id(_id=_id, db_alias=db_alias)
        if db_alias is None:
            if user is not None:
                for dbms in get_dbms_by_region(user.region):
                    self.del_user_by_id(_id, db_alias=dbms)
                    # if not success:
                    #     return False
            return True
        else:
            check_alias(db_alias)
            return user.delete()

    def del_user_by_uid(self, uid, db_alias=None):
        user = self.get_user_by_uid(uid=uid, db_alias=db_alias)
        if db_alias is None:
            if user is not None:
                for dbms in get_dbms_by_region(user.region):
                    self.del_user_by_uid(uid, db_alias=dbms)
                    # if not success:
                    #     return False
            return True
        else:
            check_alias(db_alias)
            return user.delete()

    @staticmethod
    def pretty_users(users):
        pretty_models(users, UserService.field_names)
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
