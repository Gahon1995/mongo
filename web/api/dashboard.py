#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-08 15:57
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from flask import request, Blueprint

from web.result import Result

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('', methods=['GET'])
def get_dashboard_info():
    from config import DBMS
    from service.user_service import UserService
    from service.article_service import ArticleService
    from service.read_service import ReadService
    from service.popular_service import PopularService
    dbms = request.args.get('dbms')

    if dbms not in DBMS().all:
        return Result.gen_failed(code=500, msg='dbms error')

    nums = {
        'users': UserService().count(db_alias=dbms),
        'articles': ArticleService().count(db_alias=dbms),
        'reads': ReadService().count(db_alias=dbms),
        'populars': PopularService().count(temporalGranularity='daily', db_alias=dbms)
    }
    nodes = get_nodes(dbms)

    charts = {
        'users': [],
        'articles': [],
        'reads': []
    }

    for dbms1 in DBMS().get_all_dbms_by_region():
        charts['users'].append({'name': dbms1, 'value': UserService().count(db_alias=dbms1)})
        charts['articles'].append({'name': dbms1, 'value': ArticleService().count(db_alias=dbms1)})
        charts['reads'].append({'name': dbms1, 'value': ReadService().count(db_alias=dbms1)})

    data = {
        'nums': nums,
        'charts': charts,
        'nodes': nodes
    }

    return Result.gen_success(data=data)
    pass


def get_nodes(dbms):
    from db.mongodb import dbs
    print(dbms)

    node = dbs[dbms].nodes
    print(node)
    return list(n[1] for n in node)
