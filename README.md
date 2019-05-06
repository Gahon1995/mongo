# 分布式数据库大作业

主要实现数据的分布式读写一些分类

## TODO
1. mongo连接失败时的异常处理
2. 阅读文章结束后异步请求保存阅读数据
3. 为mongoDB编写Docker compose文件（将数据映射到volume，方便快速部署和保存）
4.  ~~为程序编写Dockerfile文件（暂时应该不用)~~
5. ~~编写controller层，调用相关接口返回json格式数据（编写web端时在考虑）~~
6. mongoDB切片部署
7. Hadoop的部署
8. redis的部署
9. 全局异常捕获

## 已完成
1. 各个数据表的设计
2. 对mongoDB的简单增删改查
3. mongoDB数据库测试数据生成代码的编写
4. 更多功能见cmd-ui下