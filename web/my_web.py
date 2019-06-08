#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-08 15:17
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

import logging
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from utils.func import singleton


@singleton
class Web:
    session = None
    jwt = None
    log = None

    def __init__(self):
        self.session = Flask(__name__)
        self.log = logging.getLogger('werkzeug')
        # self.log.setLevel(logging.ERROR)

        self.register_blueprint()
        self.session.config['JWT_SECRET_KEY'] = 'secret'  # 目前都是本地，暂不用放配置文件
        self.session.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=60 * 60 * 24 * 7)  # Token 超时时间 7 天
        self.jwt = JWTManager(self.session)
        CORS(self.session, supports_credentials=True)

    def register_blueprint(self):
        from web.api.user import users
        from web.api.dashboard import dashboard
        from web.api.article import articles
        self.session.register_blueprint(users, url_prefix='/api/users')
        self.session.register_blueprint(articles, url_prefix='/api/articles')
        self.session.register_blueprint(dashboard, url_prefix='/api/dashboard')

    @classmethod
    def run(cls):
        self = cls()
        self.start()

    def start(self):
        self.run_session()
        # if not Config().WEB_ENABLE or Config().is_slave(): return
        # if Config().IS_DEBUG:
        #     self.run_session()
        # else:
        # create_thread_and_run(self, 'run_session', wait=False)

    def run_session(self):
        # debug = False
        debug = Config().IS_DEBUG
        self.session.run(debug=debug, port=Config().WEB_PORT, host='0.0.0.0')


if __name__ == '__main__':
    from main import init

    init()

    Web().run()
