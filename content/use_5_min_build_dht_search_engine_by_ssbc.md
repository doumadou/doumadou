Title: 5分钟搭建自己的磁力搜索网站
Category: Other
Tags: docker
Date: 2015-08-04 15:24:15
Author: Gavin



本文基于SSBC(手撕包菜) + docker搭建

环境说明:
	搜索引擎使用的是小虾的开源ssbc
	docker环境是我做最简单的镜像
	VPS用的是DigitOcean提供的ubuntu14.04带docker的镜像生成的vps

	没有DigitOcean账号的，可通过如下链接注册，账号注册成功，可得10$的（相当于免费使用2个月）.

好了，啥也不说了，一步一步按照我的步聚开工吧!

##准备工作

DigitOcean上创建vps.

##第一步下载代码
	
	# yum install -y git
	# git clone https://github.com/doumadou/ssbc

##下载docker 镜像

	# docker pull doumadou/cili_s_s_b_c:centos7
	# docker images

如果存在cili_s_s_b_c则说明镜像下载成功了


##启动网站

	# docker run -d 

##查看效果

现在通过IP地址在本地打开我们刚才搭建的磁力搜索引擎

效果如下：




我们过十分钟再看一下爬虫采集的效果。

十分钟后，我的查看a的相关数据效果如下：

磁力搜索引擎网站相关信息如下:
数据库用户名: root 密码: root
搜索引擎后台用户名: root 密码: root
