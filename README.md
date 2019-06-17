# 分布式数据库大作业

主要实现数据的分布式读写一些分类

# 使用方法

## 配置文件`config.py`说明

该文件为该项目的主要配置文件，其主要的配置项在里边都有说明，需要注意的一点是需要根据自己的电脑配置进行 DBMS 的配置，而且在使用单 MongoDB 和有复制节点的 mongodb 时，有`gethost`方法是需要修改一下的。

另外关于服务器端的配置请看 server 下边的 README.md 文件

# PS

由于时间有限，该项目还有很多不完善的地方，同时对于该项目的说明文档写得也很少，有可能你看了跟着配置不出来，如果在配置的时候出现报错，请 Google 解决，应该都很容易解决的。

另外如果要在虚拟机上进行配置的话，有可能会出现更多的问题，因为涉及到端口映射的问题，所以建议使用没有复制集的 mongdb 版本进行测试，这样能够避免很多坑
