#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-04 22:25
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from flask import request
from flask.views import MethodView

from config import DBMS
from service.be_read_service import BeReadService
from service.read_service import ReadService
from service.user_service import UserService
from utils.func import get_best_dbms_by_category, timestamp_to_str
from web.api.result import Result


class ArticleRecord(MethodView):
    def get(self, aid):

        category = request.args.get('category')
        if category is not None:

            if category not in DBMS().category['values']:
                return Result.gen_failed('404', '类别不存在')

        record = {}

        be_read = BeReadService().get_one_by_aid(aid,
                                                 exclude=['readUidList', 'agreeUidList', 'shareUidList'],
                                                 db_alias=get_best_dbms_by_category("technology"))
        print(be_read)
        if be_read is not None:
            record = be_read.to_dict(
                exclude=['commentUidList', 'readUidList', 'agreeUidList', 'shareUidList'])
            comments = []
            for uid in be_read.commentUidList:
                comment = None
                user = None
                for dbms in DBMS().get_all_dbms_by_region():
                    comment = ReadService().get_by_uid_and_aid(uid=int(uid),
                                                               aid=int(aid),
                                                               only=['rid', 'commentDetail', 'timestamp'],
                                                               db_alias=dbms)
                    if comment is not None:
                        user = UserService().get_user_by_uid(uid=uid, db_alias=dbms, only=['name'])
                        break

                if comment is not None and user is not None:
                    comments.append(
                        {'rid': comment.rid,
                         'name': user.name,
                         'commentDetail': comment.commentDetail,
                         'timestamp': timestamp_to_str(comment.timestamp)
                         })
            record['comments'] = comments
        return Result.gen_success(data=record)
