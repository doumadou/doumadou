Title: docker使用笔记
Category: docker 
Tags: 
Date: 2015-09-17 12:10:16
---


1 删除使用某个镜像创建的所有容器

~~~
docker ps -a |grep octopus:latest |awk '{print $NF}'|xargs docker rm -f
~~~

2 expose 与 docker -p 参数

Dockerfile中的EXPOSE、docker run --expose、docker run -p之间的区别
Dockerfile的EXPOSE相当于docker run --expose，提供container之间的端口访问。docker run -p允许container外部主机访问container的端口
