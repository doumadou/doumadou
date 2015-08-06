Title: 5分钟搭建自己的磁力搜索网站
Category: Other
Tags: docker
Date: 2015-08-04 15:24:15
Author: Gavin



本文基于SSBC(手撕包菜) + docker搭建

环境说明:

搜索引擎使用的是小虾的开源ssbc

docker镜像是我做最简单的镜像

VPS用的是DigitOcean提供的ubuntu14.04带docker的镜像生成的vps

没有DigitOcean账号的，可通过如下链接(https://www.digitalocean.com/?refcode=57030d16bf16)注册，账号注册成功，可得10$的（相当于免费使用2个月）.

[账号注册](https://www.digitalocean.com/?refcode=57030d16bf16){:target="_blank"}


好了，啥也不说了，一步一步按照我的步聚开工吧!

##准备工作

DigitOcean上创建vps.

Applcation选择docker镜像

如下图所示：

![DigitOcean镜像选择docker](/images/20150804003313.png)

##第一步下载代码
	
	# git clone https://github.com/doumadou/ssbc

##下载docker 镜像


速度很快，几分钟就搞定了

	root@ssbc:~# docker pull doumadou/cili_s_s_b_c:centos7
	Pulling repository doumadou/cili_s_s_b_c
	e1583d9521f4: Download complete 
	436cb282cd02: Download complete 
	21af27143b54: Download complete 
	d28e315add15: Download complete 
	ecf3924b28e9: Download complete 
	2f1d5de57db2: Download complete 
	f06e14257d37: Download complete 
	5a7cb6bb4a0e: Download complete 
	a19d83d19ff8: Download complete 
	b4db54995744: Download complete 
	ee71504a9dce: Download complete 
	Status: Downloaded newer image for doumadou/cili_s_s_b_c:centos7


	root@ssbc:~# docker images
	REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	doumadou/cili_s_s_b_c   centos7             e1583d9521f4        12 days ago         934.9 MB

如果存在cili_s_s_b_c则说明镜像下载成功了


##启动网站

	# docker run -d --net=host -v /root/ssbc:/home/wwwroot/ssbc doumadou/cili_s_s_b_c:centos7
	b82fe943afecaab6bb15bfe4f9f9abe001d6ef51971c729fab3c7479f3ea2603

说明网站及爬虫启动成功。

##查看效果

现在通过IP地址在本地打开我们刚才搭建的磁力搜索引擎

效果如下：

![磁力网站首页](/images/20150804004642.png)


我们过十分钟再看一下爬虫采集的效果。

十分钟后，我的查看a的相关数据效果如下：

![磁力网站搜索结果页](/images/20150806232048.png)

磁力搜索引擎网站相关信息如下:
数据库用户名: root 密码: root
搜索引擎后台用户名: root 密码: root

再看后台效果:

![磁力网站搜索网站后台](/images/20150806232511.png)
