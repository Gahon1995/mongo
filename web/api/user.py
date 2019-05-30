from flask import request
from flask.views import MethodView

from service.user_service import UserService
from utils.result import Result


class UserGetUpdateDelete(MethodView):
    def get(self, uid):
        user = UserService().get_user_by_uid(uid=uid)
        if user is None:
            return Result.gen_failed(404, 'user not found')
        return Result.gen_success(user.to_dict())
        pass

    def put(self, uid):
        pass

    def delete(self, uid):
        if uid is None:
            return Result.gen_failed('404', 'uid not found')

        return Result.gen_success('删除成功')


class UsersList(MethodView):
    # @jwt_required
    def get(self):
        page_num = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 20))
        region = request.args.get('region')
        kwargs = {}
        if region is not None:
            kwargs['region'] = region
        res = UserService().get_users(page_num=page_num, page_size=page_size, **kwargs)
        users = list()
        total = UserService().count_all()
        for user in res:
            users.append(user.to_dict())
        data = {'total': total, 'list': list(users)}
        return Result.gen_success(data)

    # def post(self):
    #     page_num = int(request.args.get('page_num', 1))
    #     page_size = int(request.args.get('page_size', 20))
    #     res = UserService().get_users(page_num=page_num, page_size=page_size, db_alias=DBMS.DBMS1)
    #     users = list()
    #     for user in res:
    #         users.append(user.to_dict())
    #
    #     return jsonify(list(users))

    def put(self):
        pass

    def delete(self):
        pass
