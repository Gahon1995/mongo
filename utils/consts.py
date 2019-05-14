#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 16:45
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from enum import Enum


class Gender(Enum):
    male = 0
    female = 1


class Region(Enum):
    bj = 'bj'
    hk = 'hk'


class Language(Enum):
    zh = 0
    eng = 1


class Const:
    gender = {'male', 'female'}
    region = {}
    language = {}
    role = {}
    grade = {}
