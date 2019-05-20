#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 20:43
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import logging

from bson import ObjectId

from model.read import Read
from service.be_read_service import BeReadService
from service.ids_service import IdsService
from service.user_service import UserService
from utils.func import *

logger = logging.getLogger('ReadService')


@singleton
class ReadService(object):
    field_names = ['aid', 'uid', 'readOrNot', 'readTimeLength', 'readSequence', 'agreeOrNot', 'commentOrNot',
                   'shareOrNot', 'commentDetail', 'timestamp']

    @staticmethod
    def get_model(dbms: str):
        class Model(Read):
            meta = {
                'db_alias': dbms,
                'collection': 'read'
            }
            pass

        return Model

    @staticmethod
    def get_id():
        """
            通过去ids表中查询得到当前read表中下一个rid的理论值（因为还得根据region进行判断
        :return: rid
        """
        return IdsService().next_id('rid')

    def count(self, db_alias=None, **kwargs):
        """
            查询对应数据库中的read记录总数
        :param db_alias:    待查询的数据库名称
        :param kwargs:      高级查询条件，详细用法见mongo engine用法
        :return:
        """
        check_alias(db_alias)
        return self.get_model(db_alias).count(**kwargs)

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
        user = UserService().get_user_by_uid(uid)
        if user is None:
            return None
        rid = self.get_id()

        new_read = None
        # 根据用户的region去查询当前region对应的所有数据库
        for dbms in get_dbms_by_region(user.region):
            new_read = self.__save_read(rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot,
                                        commentDetail, agreeOrNot, shareOrNot, timestamp, db_alias=dbms)
            if new_read is None:
                break

        # 待修改
        BeReadService().add_be_read_record(aid, uid, readOrNot, commentOrNot, agreeOrNot, shareOrNot, timestamp)

        return new_read

    def __save_read(self, rid, aid, uid, readOrNot, readTimeLength, readSequence, commentOrNot, commentDetail,
                    agreeOrNot, shareOrNot, timestamp=None, db_alias=None):
        # 在db_alias 所选中的数据库中 建立实例保存read数据
        check_alias(db_alias)

        new_read = self.get_model(db_alias)()
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
        new_read.timestamp = timestamp or get_timestamp()
        logger.info("save read to dbms:{}, record: aid: {}, uid: {}".format(db_alias, aid, uid))
        new_read.save()
        return new_read

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
            return self.get_model(db_alias).list_by_page(page_num, page_size, **kwargs)

    def del_read_by_id(self, _id, db_alias=None):
        """
            通过rid进行删除， 如果不指定数据库的话将在所有数据库中查询
        :param _id:
        :param db_alias:
        :return:   1： 删除成功
                    0： 当前数据库没有rid信息
        """
        del_num = 0
        if db_alias is None:
            for dbms in DBMS.all:
                del_num += self.del_read_by_id(_id, db_alias=dbms)
        else:
            check_alias(db_alias)
            if not isinstance(_id, ObjectId):
                _id = ObjectId(_id)
            del_num = self.get_model(db_alias).objects(id=_id).delete()
        return del_num

    def del_reads_by_uid(self, uid: int, db_alias=None):
        """
            通过uid进行删除该uid对应的所有历史记录， 如果不指定数据库的话将在所有数据库中查询
        :param uid:
        :param db_alias:
        :return:  0： 当前数据库没有该uid对应的记录
                 >0: 删除的记录条数
        """
        del_num = 0
        if db_alias is None:
            user = UserService().get_user_by_uid(uid)
            if user is None:
                logger.info("删除不存在的用户'{}'的记录".format(uid))
                return 0
            for dbms in get_dbms_by_region(user.region):
                del_num += self.del_reads_by_uid(uid, db_alias=dbms)
        else:
            check_alias(db_alias)
            del_num = self.get_model(db_alias).objects(uid=uid).delete()
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
        user = UserService().get_user_by_uid(uid)
        if user is None:
            return []
        return self.__get_history(uid, page_num, page_size, db_alias=get_best_dbms_by_region(user.region))

    def __get_history(self, uid, page_num=1, page_size=20, db_alias=None):
        check_alias(db_alias)
        return self.get_model(db_alias).list_by_page(page_num, page_size, uid=uid)

    def compute_popular(self, end_date: datetime.date, before_days, top_n=10):
        """
            计算 end_date 这天结束 到 before_days 之间各篇文章阅读的频率
        :param end_date:    date格式，一般传入当天时间
        :param before_days:
        :param top_n:
        :return:
        """

        freq_all = dict()

        def get_date_timestamp(_date):
            # 根据date计算第二天0点的timestamp
            _re = datetime.datetime.strptime(str("{}-{}-{}".format(_date.year, _date.month, _date.day + 1)), '%Y-%m-%d')
            return int(_re.timestamp() * 1000)

        start = get_date_timestamp(end_date - datetime.timedelta(days=before_days))
        end = get_date_timestamp(end_date)
        for dbms in DBMS.all:
            #  TODO 比较 aggregate 和 item_frequencies 的性能差距
            # freq = self.__get_popular_by_freq(start, end, top_n * 2, db_alias=dbms)
            # print(freq)
            freq = self.__get_popular_by_aggregate(start, end, top_n * 2, db_alias=dbms)
            freq_all = merge_dict(freq_all, freq)

        return sort_dict(freq_all)[:top_n]

    def __get_popular_by_freq(self, start, end, top_n=20, db_alias=None):
        check_alias(db_alias)

        return self.get_model(db_alias).objects(timestamp__gte=start, timestamp__lte=end).item_frequencies('aid')
        pass

    def __get_popular_by_aggregate(self, start, end, top_n=20, db_alias=None):
        check_alias(db_alias)
        #  TODO 比较 aggregate 和 item_frequencies 的性能差距
        freq = self.get_model(db_alias).objects(timestamp__gte=start, timestamp__lte=end).aggregate(
            {'$group': {'_id': '$aid', 'count': {'$sum': 1}}})

        re = dict()
        for item in freq:
            re[item['_id']] = item['count']

        return re

    def get_daily_popular(self, end_date: datetime.date, before_days=1, top_n=10):
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
        return self.compute_popular(end_date, before_days, top_n)

    def get_weekly_popular(self, end_date: datetime.date, before_days=7, top_n=10):
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
        return self.compute_popular(end_date, before_days, top_n)

    def get_monthly_popular(self, end_date: datetime.date, before_days=30, top_n=10):
        if isinstance(end_date, datetime.datetime):
            end_date = end_date.date()
        return self.compute_popular(end_date, before_days, top_n)

    @staticmethod
    def pretty_reads(reads):
        pretty_models(reads, ReadService.field_names)
