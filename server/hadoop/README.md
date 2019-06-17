### Hadoop 部署说明

由于是伪分布式，所以需要设置 hostname

使用 hadoop 需要将下边的添加到电脑的 hosts 里边

> your_ip datanode  
> your_ip historyserver  
> your_ip namenode  
> your_ip nodemanager  
> your_ip resourcemanager

如果使用虚拟机的话还需要将虚拟机这些服务对应的端口映射到对应的虚拟机中去
