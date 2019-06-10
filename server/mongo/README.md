## MongoDB Server 部署说明

### 文件夹

- bj_multi


### 部署说明

在部署docker镜像之前需要先在host主机，也就是这个项目代码运行的主机上运行 `hostname
\-f` 来获取当前的主机名，然后修改`docker-compose.yml`
文件中rs-setup的environment中的变量为当前的主机名

另外需要修改当前主机的hosts，将mongo-1-1 mono-2-1... 添加到hosts中去
