from mongoengine import Document, connect, register_connection, DoesNotExist
from mongoengine.context_managers import switch_db
from utils.func import convert_mongo_2_json, utc_2_local
import functools
import logging

logger = logging.getLogger('db')


class BaseDB(Document):
    meta = {
        'abstract': True,
    }

    def __str__(self):
        #     # 重写str方法， 将ObjectId 和datetime格式正确的输出
        return convert_mongo_2_json(self)

    def get_create_time(self):
        if self.id is None:
            return None
        return self.id.generation_time

    @classmethod
    def list_by_page(cls, page_num=1, page_size=20, **kwargs):
        """
            分页数据查询

        :param page_num: 查询的页码，默认第一页
        :param page_size: 每一页显示的数量
        :param kwargs: 查询的条件
        :return: 符合条件的分页数后据
        """
        offset = (page_num - 1) * page_size
        return cls.objects(**kwargs).skip(offset).limit(page_size)

    @classmethod
    def count(cls, **kwargs):
        """

        :return: 当前数据的总量
        """
        return cls.objects(**kwargs).count()

    @classmethod
    def find(cls, **kwargs):
        """
            查询所有数据（未分页）
        :param kwargs: 查询条件
        :return:
        """
        return cls.objects(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        """
        返回符合条件的所有值的第一个

        :param kwargs: 查询条件
        :return:
        """
        return cls.objects(**kwargs).first()

    @classmethod
    def get(cls, **kwargs):
        """
        获取一个unique的项

        :param kwargs: 查询条件
        :return:
        """
        try:
            user = cls.objects(**kwargs).get()
            return user
        except DoesNotExist:
            return None

    @classmethod
    def insert_one(cls, data: str):
        """
            插入一条数据
            由于加入了引用，所以该方法使用会出错
            TODO 去掉该方法以及该方法的相关引用

        :param data: 插入的数据类容，需要符合cls的类型
        :return:
        """
        return cls.from_json(data).save()

    @classmethod
    def insert_many(cls, data: list):
        """
            插入数据需要为list，否则报错

        :param data:
        :return:
        """
        if isinstance(data, list):
            for d in data:
                cls.from_json(d).save()
            return True
        else:
            raise BaseException('data type error, should be a list')

    @classmethod
    def delete_by(cls, **kwargs):
        """
            删除符合条件的数据
        :param kwargs:
        :return:
        """
        return cls.objects(**kwargs).delete()

    @classmethod
    def get_id(cls, _id: str):
        """
            查询当前最大的id

        :param _id: 当前class 的id 名称
        :return:
        """

        obj = cls.objects.order_by('-' + _id).limit(1).first()
        if obj is None:
            return 1
        else:
            return int(obj.__getattribute__(_id)) + 1


def init_connect():
    """
        初始化mongo连接， 不传参数则从Config文件中读取
        默认连接北京节点，然后分别注册两个节点的信息
    :return:
    """
    from Config import Config
    from utils.consts import DBMS
    # tz_aware=True 设置时区修正，mongoDB的时区默认为UTC0，需要加上这个加入时区信息
    connect(Config.mongo_db_name, host=Config.bj_mongo_host, port=Config.bj_mongo_port, tz_aware=True)
    # connect(Config.mongo_db_name)
    register_connection(alias=DBMS.DBMS1, db=Config.mongo_db_name, host=Config.bj_mongo_host,
                        port=Config.bj_mongo_port,
                        tz_aware=True)
    register_connection(alias=DBMS.DBMS2, db=Config.mongo_db_name, host=Config.hk_mongo_host,
                        port=Config.hk_mongo_port, tz_aware=True)


from utils.func import DbmsAliasError
from utils.consts import DBMS


def switch_mongo_db(cls, default_db=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                db_alias = kwargs.get('db_alias')
                if db_alias is None:
                    db_alias = default_db
                if not (db_alias == DBMS.DBMS1 or db_alias == DBMS.DBMS2):
                    raise DbmsAliasError('db_alias error, {}'.format(db_alias))
                # print("switch db: cls={0}, db_alias={1}".format(cls.__name__, db_alias))
                logger.debug("switch db: cls={0}, db_alias={1}".format(cls.__name__, db_alias))
                with switch_db(cls, db_alias):
                    return func(*args, **kwargs)
            except KeyError:
                logger.warning("没有指定数据库连接，使用默认数据库连接")
                return func(*args, **kwargs)

        return wrapper

    return decorator
