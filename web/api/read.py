from flask import request
from flask.views import MethodView

from service.read_service import ReadService
from utils.func import check_alias, DbmsAliasError
from web.api.result import Result


class ReadCURD(MethodView):
    def get(self, rid):
        read = ReadService().get_by_rid(rid=rid)
        if read is None:
            return Result.gen_failed(404, 'user not found')
        return Result.gen_success(read.to_dict())
        pass

    def put(self, rid):
        pass

    def delete(self, rid):
        if rid is None:
            return Result.gen_failed('404', 'uid not found')

        return Result.gen_success('删除成功')


class ReadsList(MethodView):
    # @jwt_required
    def get(self):
        page_num = int(request.args.get('page', 1))
        page_size = int(request.args.get('size', 20))
        region = request.args.get('region')
        uid = request.args.get('uid')
        rid = request.args.get('rid')

        dbms = request.args.get('dbms')
        try:
            check_alias(db_alias=dbms)
        except DbmsAliasError:
            return Result.gen_failed('404', 'dbms error')

        cons = {
            'region': region,
            'uid': uid,
            'rid': rid
        }
        kwargs = {}
        for key, value in cons.items():
            if value is not None:
                kwargs[key] = value

        res = ReadService().get_reads(page_num=page_num, page_size=page_size, db_alias=dbms, **kwargs)
        reads = list(read.to_dict() for read in res)
        total = ReadService().count(db_alias=dbms)
        data = {'total': total, 'list': reads}
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

    def delete(self, rid):
        if rid is None:
            return Result.gen_failed('404', 'aid not found')

        # ReadService().del_read_by_rid(rid)

        return Result.gen_success('删除成功')
