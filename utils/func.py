#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019-04-29 14:31
# @Author  : Gahon
# @Email   : Gahon1995@gmail.com


def show_next(page_num, page_size, total, next_func):
    total_pages = int((total - 1) / page_size) + 1
    flag = False

    print("\n\t\t\t\t\t当前第{page_num}页， 总共{total_pages}页，共{total}条数据"
          .format(page_num=page_num,
                  total_pages=total_pages,
                  total=total))
    if total_pages > 1:
        flag = True
    while flag:
        print("\t\t1. 上一页\t2. 下一页\t3. 指定页数\t4.返回上一级")
        mode = input("请选择操作： ")
        if mode == '1':
            if page_num <= 1:
                print("当前就在第一页哟")
            else:
                return next_func(page_num - 1)
        elif mode == '2':
            if page_num >= total_pages:
                print("当前在最后一页哟")
            else:
                return next_func(page_num + 1)
        elif mode == '3':
            num = int(input('请输入跳转页数: '))
            if 0 < num <= total_pages:
                return next_func(num)
            else:
                print("输入页码错误")
        elif mode == '4':
            return None
    input("\n\t按回车键返回")
    pass
