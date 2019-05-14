#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-28 16:45
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com

from enum import Enum


class Gender:
    male = 'male'
    female = 'female'


class Region:
    bj = 'Beijing'
    hk = 'Hong Kong'


class DBMS:
    DBMS1 = Region.bj
    DBMS2 = Region.hk


class Language:
    zh = 'zh'
    eng = 'eng'


class Category:
    science = 'science'
    technology = 'technology'
