# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-05-10 21:06
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com
import genDatabase as gen
from config import DBMS
from main import init


class TestBase:

    # 每个方法执行前运行的初始化内容
    def setup_method(self) -> None:
        pass

    # 只在运行前执行一次
    @classmethod
    def setup_class(cls) -> None:
        print("连接数据库")
        DBMS.db_name = 'test'
        init()

        gen.USERS_NUM = 100
        gen.ARTICLES_NUM = 100
        gen.READS_NUM = 100

        gen.gen_data()
        pass

    # 运行结束以后执行的内容
    def teardown_method(self) -> None:
        pass

    @classmethod
    def teardown_class(cls) -> None:
        gen.reset_db()
        pass
