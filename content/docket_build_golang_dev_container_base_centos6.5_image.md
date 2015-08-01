Title: 使用Dokefile build Golang开发环境
Category: golang
Tags: golang, Docker
Date: 2015-08-01 22:14:19
Author: Gavin


基础镜像 doumadou/centos6.5_x86_64-base:latest



Dockerfile:

~~~
	FROM doumadou/centos6.5_x86_64-base:latest
	MAINTAINER Gavin Tao "gavin.tao17@gmail.com"
	
	RUN cd /tmp  && rpm -ivh http://dl.Fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm && yum -y install golang && rm /tmp/* -rfv
~~~


生成的存储在Dockerfile的名称 doumadou/centos6.5_x86_64_golang_dev:latest
