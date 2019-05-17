#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
from bson import ObjectId

from model.read import Read
from service.ids_service import IdsService
from utils.func import *
from db.mongodb import switch_mongo_db
import logging

from service.be_read_service import BeReadService
from service.user_service import UserService

logger = logging.getLogger('ReadService')


@singleton
class ReadService(object):

    @staticmethod
    def get_id():
        """
            通过去ids表中查询得到当前read表中下一个rid的理论值（因为还得根据region进行判断
        :return: rid
        """
        # _id = -1
        # for dbms in DBMS.all:
        #     _id = max(ReadService.__id(db_alias=dbms), _id)
        # return _id
        return IdsService().next_id('rid')

    # @staticmethod
    # @switch_mongo_db(cls=Read)
    # def __id(db_alias=None):
    #     check_alias(db_alias)
    #     return Read.get_id('rid')

    @switch_mongo_db(cls=Read)
    def count(self, db_alias=None, **kwargs):
        """
            查询对应数据库中的read记录总数
        :param db_alias:    待查询的数据库名称
        :param kwargs:      高级查询条件，详细用法见mongo engine用法
        :return:
        """
        check_alias(db_alias)
        return Read.count(**kwargs)

    def save_read(self, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot, commentDetail, agreeOrNot,
                  shareOrNot, timestamp=None):
        """
            保存一个新的read记录
        :param aid:
        :param uid:
        :param readOrNot:
        :param readTimeLength:
        :param readSequence:
        :param commentOrNot:
        :param commentDetail:
        :param agreeOrNot:
        :param shareOrNot:
        :param timestamp:
        :return:
        """
        # logger.info('save read:{}'.format(new_read))

        # 根据user的region去得到正确的rid， 因为read表分布和user的region分布式一样的
        user = UserService().get_user_by_uid(int(uid))
        rid = get_id_by_region(ReadService.get_id(), user.region)

        new_read = None
        # 根据用户的region去查询当前region对应的所有数据库
        for dbms in get_dbms_by_region(user.region):
            new_read = self.__save_read(rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot,
                                        commentDetail, agreeOrNot, shareOrNot, timestamp, db_alias=dbms)
            if new_read is None:
                break

        IdsService().set_id('rid', rid)

        # 待修改
        # BeReadService.add_be_read_record(aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, user.region,
        #                                  timestamp)

        return new_read

    @switch_mongo_db(cls=Read)
    def __save_read(self, rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot, commentDetail,
                    agreeOrNot, shareOrNot, timestamp=None, db_alias=None):
        # 在db_alias 所选中的数据库中 建立实例保存read数据
        check_alias(db_alias)

        new_read = Read()
        new_read.rid = rid
        new_read.aid = aid
        new_read.uid = uid
        new_read.readOrNot = int(readOrNot)
        new_read.readTimeLength = int(readTimeLength)
        new_read.readSequence = int(readSequence)
        new_read.commentOrNot = int(commentOrNot)
        new_read.commentDetail = commentDetail
        new_read.agreeOrNot = int(agreeOrNot)
        new_read.shareOrNot = int(shareOrNot)
        new_read.timestamp = timestamp or datetime.datetime.utcnow()
        logger.info("save to dbms:{}\nrecord: {}".format(db_alias, new_read))
        new_read.save()
        return new_read

    @switch_mongo_db(cls=Read, allow_None=True)
    def get_reads(self, page_num=1, page_size=20, db_alias=None, **kwargs):
        """
            获取read表的list
            # TODO 查询多个数据库时涉及到的分页问题需解决
        :param page_num:
        :param page_size:
        :param db_alias:    带查询的数据库名称, 为空的话则两个数据库都查询
        :param kwargs:      查询条件
        :return:
        """
        if db_alias is None:
            reads = list()
            for dbms in DBMS.all:
                tmp = self.get_reads(page_num, page_size, db_alias=dbms, **kwargs)
                for r in tmp:
                    reads.append(r)
            return reads
        else:
            check_alias(db_alias)
            return Read.list_by_page(page_num, page_size, **kwargs)

    @switch_mongo_db(cls=Read, allow_None=True)
    def del_read_by_rid(self, rid, db_alias=None):
        """
            通过rid进行删除， 如果不指定数据库的话将在所有数据库中查询
        :param rid:
        :param db_alias:
        :return:   1： 删除成功
                    0： 当前数据库没有rid信息
        """
        del_num = 0
        if db_alias is None:
            for dbms in get_dbms_by_uid(rid):
                del_num += self.del_read_by_rid(rid, db_alias=dbms)
        else:
            check_alias(db_alias)
            del_num = Read.objects(rid=rid).delete()
        return del_num

    @switch_mongo_db(cls=Read, allow_None=True)
    def del_reads_by_uid(self, uid, db_alias=None):
        """
            通过uid进行删除该uid对应的所有历史记录， 如果不指定数据库的话将在所有数据库中查询
        :param uid:
        :param db_alias:
        :return:  0： 当前数据库没有该uid对应的记录
                 >0: 删除的记录条数
        """
        del_num = 0
        if db_alias is None:
            for dbms in get_dbms_by_uid(uid):
                del_num += self.del_reads_by_uid(uid, db_alias=dbms)
        else:
            check_alias(db_alias)
            del_num = Read.objects(uid=uid).delete()
        return del_num

    def get_history(self, uid, page_num=1, page_size=20):
        """
                查询uid的所有历史记录，默认20分页
        :param uid:
        :param page_num:
        :param page_size:
        :return:
        """
        # 选择一个连接最好的节点进行历史记录查询
        return self.__get_history(uid, page_num, page_size, db_alias=get_best_dbms_by_uid(uid))

    @switch_mongo_db(cls=Read)
    def __get_history(self, user, page_num=1, page_size=20, db_alias=None):
        check_alias(db_alias)
        return Read.list_by_page(page_num, page_size, uid=user)

    def calu_popular(self, end_date, before_days, top_n=10):
        if isinstance(end_date, datetime.date):
            end_date = datetime.datetime.strptime(
                str("{}-{}-{}".format(end_date.year, end_date.month, end_date.day + 1)), '%Y-%m-%d')
        # if isinstance(end_date, datetime.datetime):
        #     start = ObjectId.from_datetime(utc_2_local(end_date - datetime.timedelta(days=before_days)))
        #     end = ObjectId.from_datetime(utc_2_local(end_date))
        # else:
        #     print("查询日期格式不对，需要datetime或date类型")
        #     return None

        start = utc_2_local(end_date - datetime.timedelta(days=before_days))
        end = utc_2_local(end_date)
        for dbms in DBMS.all:
            freq = self._get_popular(start, end, top_n * 2, db_alias=dbms)

    @switch_mongo_db(cls=Read)
    def get_popular(self, start, end, top_n=20, db_alias=None):
        check_alias(db_alias)
        re = Read.objects(timestamp__gt=start, timestamp__lt=end).aggregate(
            {'$group': {'_id': '$aid', 'count': {'$sum': 1}}})
        return sort_dict_in_list(list(re), sort_by='count')[:top_n]
        pass

    @staticmethod
    def get_daily_popular(end_date, before_days=1, top_n=10, db_alias=None):
        return ReadService.calu_popular(end_date, before_days, top_n, db_alias=db_alias)

    @staticmethod
    def get_weekly_popular(end_date, before_days=7, top_n=10, db_alias=None):
        return ReadService.calu_popular(end_date, before_days, top_n, db_alias=db_alias)

    @staticmethod
    def get_month_popular(end_date, before_days=30, top_n=10, db_alias=None):
        return ReadService.calu_popular(end_date, before_days, top_n, db_alias=db_alias)

    @staticmethod
    def pretty_reads(reads):
        from prettytable import PrettyTable
        from datetime import datetime

        x = PrettyTable()

        if not isinstance(reads, list):
            reads = list(reads)
        field_names = (
            'rid', 'uid', 'readOrNot', 'readTimeLength', 'readSequence', 'agreeOrNot', 'commentOrNot',
            'shareOrNot', 'commentDetail', 'timestamp')
        x.field_names = field_names
        for read in reads:
            # 需要对时间进行时区转换
            x.add_row(list(getattr(read, key).astimezone()
                           if isinstance(getattr(read, key), datetime)
                           else getattr(read, key) for key in field_names))

        print(x)
        pass
