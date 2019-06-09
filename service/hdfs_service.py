#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-06-09 23:40
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from hdfs import InsecureClient, HdfsError

from utils.singleton import singleton


@singleton
class HDFSService(object):

    def __init__(self):
        self.hdfs = InsecureClient('http://127.0.0.1:9870', user='root')
        self.base_path = '/users/root'

    def mkdir(self, path):
        return self.hdfs.makedirs(path)

    def list(self, path):
        try:
            return self.hdfs.list(path)
        except HdfsError as e:
            print(e)
            return []

    def get(self, path):
        pass

    def upload(self, path, local_path=None, data=None):
        path = self.base_path + path
        if data is not None:
            return self.hdfs.write(path, data=data)
        elif local_path is not None:
            return self.hdfs.upload(path, local_path)
        return False
        pass

    def download(self, path):
        with self.read(path) as reader:
            buf = reader.read()
        return buf
