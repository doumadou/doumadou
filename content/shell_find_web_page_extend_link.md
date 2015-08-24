Title: 利shell命令获取某个网页的外部链接
Category: linux
Tags: 
Date: 2015-08-18 14:11:29
---



~~~shell
curl www.hao123.com | grep -Eo 'href="http://([^"]*?)"' |grep -v "www.hao123.com"
~~~shell
