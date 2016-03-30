Title: Use Pelican write blog
Date: 2015-07-14 15:49
Category: Python
Tags: pelican, publishing
Slug: try-pelican-write_blog
Author: Gavin
Summary: try pelican write blog


##环境
   ubuntu 12.04

##安装pelican, 及依赖

    # apt-get install python-pip
    # pip install pelican
    # pip install markdown

##快速建立一个Blog

	$ mkdir blog
	$ cd blog
	$ pelican-quickstart

##写一篇文章
	文章保存路径 content目录下
	例如hello.md

	$ vim content/hello.md

内容如下

	Title: Use Pelican write blog
	Date: 2015-07-14 15:49
	Category: Python
	Tags: pelican, publishing
	Slug: try-pelican-write_blog
	Author: Gavin
	Summary: try pelican write blog
	
	
	0. 环境
	   ubuntu 12.04
	
	1. 安装pelican, 及依赖
	
##生成html文件

	$ make html

Done: Processed 1 article, 0 drafts, 0 pages and 0 hidden pages in 0.37 seconds.
说明html生成成功

##启动http服务打开 http://127.0.0.1:8000 即可看到blog站点

	$ make devserver

Done: Processed 1 article, 0 drafts, 0 pages and 0 hidden pages in 0.17 seconds.
Pelican and HTTP server processes now running in background.
说明服务启动成功

##注意事项

make html提示没有文件生成. 可能是没有安装markdown. 可以使用make html DEBUG=1看看哪里出问题了

参考文件: markdown语法

	http://www.appinn.com/markdown/
