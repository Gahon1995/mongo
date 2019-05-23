from flask import request, jsonify
from flask.views import MethodView

from config import DBMS
from service.user_service import UserService


class UserGetUpdateDelete(MethodView):
    def get(self, uid):
        user = UserService().get_user_by_uid(uid=uid)
        if user is None:
            return jsonify({})
        return jsonify(user.to_dict())
        pass

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


class UsersList(MethodView):
    def get(self):
        page_num = int(request.args.get('page_num', 1))
        page_size = int(request.args.get('page_size', 20))
        res = UserService().users_list(page_num=page_num, page_size=page_size, db_alias=DBMS.DBMS1)
        users = list()
        for user in res:
            users.append(user.to_dict())

        return jsonify(list(users))

    def post(self):
        page_num = int(request.args.get('page_num', 1))
        page_size = int(request.args.get('page_size', 20))
        res = UserService().users_list(page_num=page_num, page_size=page_size, db_alias=DBMS.DBMS1)
        users = list()
        for user in res:
            users.append(user.to_dict())

        return jsonify(list(users))

    def put(self):
        pass

    def delete(self):
        pass
