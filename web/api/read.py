from flask import request
from flask.views import MethodView

from config import DBMS
from service.be_read_service import BeReadService
from service.read_service import ReadService
from service.redis_service import RedisService
from utils.func import check_alias, DbmsAliasError, get_dbms_by_region, get_dbms_by_category
from web.api.result import Result


class ReadCURD(MethodView):
    def get(self, rid):
        # _REDIS_KEY_ = f"READ:{rid}"
        read = ReadService().get_by_rid(rid=rid)
        if read is None:
            return Result.gen_failed(404, 'user not found')
        return Result.gen_success(read.to_dict())
        pass

    def post(self, rid):

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

        dbms = request.args.get('dbms')
        try:
            check_alias(db_alias=dbms)
        except DbmsAliasError:
            return Result.gen_failed('404', 'dbms error')

        uid = request.args.get('uid')
        aid = request.args.get('aid')
        cons = {
            'uid': uid,
            'aid': aid
        }
        kwargs = {}
        for key, value in cons.items():
            if value is not None and value != '':
                kwargs[key] = value

        _REDIS_KEY_ = f"READ_LIST:{dbms}:{page_num}:{page_size}:{kwargs}"
        data = RedisService().get_redis(dbms).get_dict(_REDIS_KEY_)
        if data is None or data == {}:
            res = ReadService().get_reads(page_num=page_num, page_size=page_size, db_alias=dbms, **kwargs)
            reads = list(read.to_dict() for read in res)
            total = ReadService().count(db_alias=dbms, **kwargs)
            data = {'total': total, 'list': reads}

            RedisService().get_redis(dbms).set_dict(_REDIS_KEY_, data)
        return Result.gen_success(data)

    def post(self):
        # TODO uid 和region 通过登录的用户进行获取
        # print(request.json)
        uid = int(request.json.get('uid'))
        aid = int(request.json.get('aid'))
        region = request.json.get('region')
        category = request.json.get('category')

        readOrNot = int(request.json.get('readOrNot', 0))
        readTimeLength = int(request.json.get('readTimeLength', 0))
        readSequence = int(request.json.get('readSequence', 0))
        agreeOrNot = int(request.json.get('agreeOrNot', 0))
        commentOrNot = int(request.json.get('commentOrNot', 0))
        shareOrNot = int(request.json.get('shareOrNot', 0))
        commentDetail = request.json.get('commentDetail', '')

        if region not in DBMS().region['values'] or category not in DBMS().category['values']:
            return Result.gen_failed(500, msg='region or category error')

        if uid is None or aid is None:
            return Result.gen_failed(500, "uid or aid 不能为空")

        rid = -343
        for dbms in get_dbms_by_region(region):
            rid = ReadService().new_record(aid=aid,
                                           uid=uid,
                                           readOrNot=readOrNot,
                                           readTimeLength=readTimeLength,
                                           readSequence=readSequence,
                                           agreeOrNot=agreeOrNot,
                                           commentOrNot=commentOrNot,
                                           shareOrNot=shareOrNot,
                                           commentDetail=commentDetail,
                                           db_alias=dbms).rid

        for dbms in get_dbms_by_category(category):
            BeReadService().new_record(aid=aid,
                                       uid=uid,
                                       readOrNot=readOrNot,
                                       commentOrNot=commentOrNot,
                                       agreeOrNot=agreeOrNot,
                                       shareOrNot=shareOrNot,
                                       db_alias=dbms)

        return Result.gen_success(msg='success', data={'rid': rid})
        pass

    def put(self):
        pass

    # def delete(self, rid):
    #     if rid is None:
    #         return Result.gen_failed('404', 'aid not found')
    #
    #     # ReadService().del_read_by_rid(rid)
    #
    #     return Result.gen_success('删除成功')
