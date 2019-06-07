import logging

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, current_user

from config import DBMS
from service.redis_service import RedisService
from service.user_service import UserService
from utils.func import check_alias, DbmsAliasError
from web.api.result import Result

logger = logging.getLogger("API_USER")


class UserGetUpdateDelete(MethodView):
    def get(self, uid):
        user = {}
        _REDIS_KEY_ = f"USER:{uid}"
        for dbms in DBMS().get_all_dbms_by_region():
            user = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
            if user != {}:
                break

        if user is None or user == {}:
            logger.info("get from mongodb")
            user = UserService().get_user_by_uid(uid=uid)
            if user is None:
                return Result.gen_failed(404, 'user not found')

            user = user.to_dict()

            RedisService().get_redis(DBMS().get_best_dbms_by_region(user['region'])).set_dict(_REDIS_KEY_, user)
        else:
            logger.info("get from redis")
        return Result.gen_success(user)
        pass

    @jwt_required
    def post(self, uid):
        """用户信息更新"""
        user = current_user
        is_admin = (user.name == 'admin')

        if is_admin:
            user = UserService().get_user_by_uid(uid)

        forbid = ['uid', 'pwd', 'name', 'timestamp']

        if (not is_admin) or user.uid != uid:
            Result.gen_failed(code=50001, msg='无权限进行此操作')

        if is_admin == 'admin':
            forbid = ['uid', 'pwd', 'timestamp']

        data: dict = request.json
        for key in list(data.keys())[::-1]:
            if key not in UserService.field_names or key in forbid:
                data.pop(key)
            else:
                # print(f'data: {key}: {data.get(key)}, origin: {getattr(user, key)}')
                if data.get(key) == getattr(user, key):
                    data.pop(key)

        print(data)
        if data == {}:
            return Result.gen_success(msg='无更新信息')

        for dbms in DBMS().get_dbms_by_region(user.region):
            UserService().update_by_uid_with_dbms(uid=uid, db_alias=dbms, **data)

        return Result.gen_success(msg='success')
        pass

    def delete(self, uid):
        for dbms in DBMS().get_all_dbms_by_region():
            num = RedisService().get_redis(dbms).delete(f"USER:{uid}")
            RedisService().get_redis(dbms).delete_by_pattern(pattern=f'USER_LIST:{dbms}:*')

            if num > 0:
                break

        if uid is None:
            return Result.gen_failed('404', 'uid not found')

        UserService().del_user_by_uid(uid=uid)

        return Result.gen_success('删除成功')


class UsersList(MethodView):
    # @jwt_required
    def get(self):
        page_num = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 20))
        dbms = request.args.get('dbms')
        try:
            check_alias(db_alias=dbms)
        except DbmsAliasError:
            return Result.gen_failed('404', 'dbms error')

        name = request.args.get('name')
        gender = request.args.get('gender')
        cons = {
            'name': name,
            'gender': gender
        }
        kwargs = {}
        for key, value in cons.items():
            if value is not None and value != '':
                kwargs[key] = value

        _REDIS_KEY_ = f"USER_LIST:{dbms}:{page_num}:{page_size}:{kwargs}"
        data = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
        if data is None or data == {}:
            logger.info("get from mongoDB")
            res = UserService().get_users(page_num=page_num, page_size=page_size, db_alias=dbms, **kwargs)
            users = list()
            total = UserService().count(db_alias=dbms, **kwargs)
            for user in res:
                users.append(user.to_dict())
            data = {'total': total, 'list': list(users)}
            RedisService().get_redis(dbms).set_dict(_REDIS_KEY_, data)
        else:
            logger.info("get from redis")
        return Result.gen_success(data)

    def post(self):
        """
            用户注册
        :return:
        """

        data = request.json

        data.pop('uid')
        print(data)
        success, msg = UserService().register(**data)

        if not success:
            return Result.gen_failed(code=505, msg=msg)

        return Result.gen_success(msg='success')

    def put(self):
        pass

    def delete(self):
        pass
