# 分布式数据库大作业

主要实现数据的分布式读写一些分类

## TODO
0. 添加id字段，替换默认生成的objectID（因为如果不使用这种方法的话会导致两个数据库中相同数据的id不一样）
1. mongo连接失败时的异常处理
2. 阅读文章结束后异步请求保存阅读数据
3. 为mongoDB编写Docker compose文件（将数据映射到volume，方便快速部署和保存）
4.  ~~为程序编写Dockerfile文件（暂时应该不用)~~
5. ~~编写controller层，调用相关接口返回json格式数据（编写web端时在考虑）~~
6. mongoDB切片部署
7. Hadoop的部署
8. redis的部署
9. 全局异常捕获
10. 测试使用静态方法在多并发的情况下会不会出现问题

## 已完成
1. 各个数据表的设计
2. 对mongoDB的简单增删改查
3. mongoDB数据库测试数据生成代码的编写
4. 更多功能见cmd-ui下

## 注意
1. service接口调用方法时必须传入参数db_alias,该参数用于选择所连接的数据库，
    其值为consts里边的Region类所对应的值。
2. 有的方法不需要传，比如登录，因为不知道该用户数据在哪个数据库里边，
       所以采用依次尝试登录的方式进行登录
       
db = connect(host="mongodb://127.0.0.1:30021,127.0.0.1:30022,127.0.0.1:30023/mongo?replicaSet=rs1", read_preference=ReadPreference.SECONDARY_PREFERRED)


   var cfg = {
        "_id": "rs1",
        "protocolVersion": 1,
        "members": [
            {
                "_id": 0,
                "host": "GahondeMBP.lan:30021"
            },
            {
                "_id": 1,
                "host": "GahondeMBP.lan:30022"
            },
            {
                "_id": 2,
                "host": "GahondeMBP.lan:30023"
            }
        ]
    };