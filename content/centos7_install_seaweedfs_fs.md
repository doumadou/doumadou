---
layout: post
title: Centos7.1 安装Seaweedfs.
category: 分布式文件系统
tags: [seaweedfs, weedfs, golang]
date: 2016-03-31 12:40:50
---

# Seaweedfs介绍

 【Seaweedfs以前旧版叫Weedfs】。

Seaweedfs 是一个非常优秀的由 golang 开发的分布式存储开源项目， 虽然在我刚开始关注的时候它在 github.com 上面只有 star 50+， 但是我觉得这个项目是一个几千 star 量级的优秀开源项目。 Seaweedfs 的设计原理是基于 Facebook 的一篇图片存储系统的论文 Facebook-Haystack， 论文很长，但是其实原理就几句话，可以看看 Facebook图片存储系统Haystack ， 我觉得Seaweedfs是青出于蓝而胜于蓝。

# 安装环境

* 操作系统centos7.1 x86_64
* IP地址：　192.168.122.181
* seaweedfs版本: 0.70beta, 下载地址: [https://bintray.com/chrislusf/seaweedfs/seaweedfs#](https://bintray.com/chrislusf/seaweedfs/seaweedfs#)



# 下载安装

直接下载2进制安装包，然后解压即可。

# 使用

## 启动 weed master, volume服务

在单机上运行，一个master, 2个volume。二个volume的存储目录分别是/opt/data/v1, /opt/data/v2/ 若文件夹不存在，先创建，否则启动 volume时会出错。

进入weed文件夹。
~~~ bash
 # ./weed master  -ip="0.0.0.0" -defaultReplication="001" -mdir="/opt/" &
 # ./weed volume -max=100 -mserver="localhost:9333" -dir="/opt/data/v1" -port=8083  -ip="192.168.122.181" -dataCenter="dc1" -rack="rack1" &
 # ./weed volume -max=100 -mserver="localhost:9333" -dir="/opt/data/v2" -port=8084  -ip="192.168.122.181" -dataCenter="dc1" -rack="rack1" &
~~~

## 上传，下载文件测试

###上传

要上传文件，先需要向master发送 HTTP POST, PUT, or GET 请求到 /dir/assign.  获得fid和volume服务的url。　这二个参数是将在下一步真正上传文件时需要。
~~~ bash
	# curl -X POST http://192.168.122.181:9333/dir/assign
	{"fid":"2,01d3fecb00","url":"192.168.122.181:8084","publicUrl":"192.168.122.181:8084","count":1}
~~~

再发送HTTP PUT or Post 上传文件，　url格式 上一步中拿到的服务器url + "/" + fid
~~~bash
	# curl -X PUT -F file=@/tmp/35695-20160330163513676-2100470393.jpg http://192.168.122.181:8084/2,01d3fecb00
	{"name":"35695-20160330163513676-2100470393.jpg","size":29448}
~~~
注意，file参数的文件路径前必须加'@', 否则就不是上传的文件，而变成了文件的内容为路径径字符串了. 如下命令就是文件内容为/tmp/35695-20160330163513676-2100470393.jpg了。
~~~
	# curl -X PUT -F file=/tmp/35695-20160330163513676-2100470393.jpg http://192.168.122.181:8084/2,01d3fecb00
~~~

上传也可用下面的上传方式

~~~
	# curl -F "filename=@/tmp/seaweedfs.png" http://192.168.122.181:9333/submit
{"fid":"3,025343432e","fileName":"seaweedfs.png","fileUrl":"192.168.122.181:8084/3,025343432e","size":78638}
~~~

###下载

fid: 2,01d3fecb00　','之前的volumeid, ',' 后面的又分二部分，这里不细说。本例中的volumeid为 2.

第一步，先查找volumeid对应的服务的url. 

~~~ bash
	# curl http://192.168.122.181:9333/dir/lookup?volumeId=2
{"volumeId":"2","locations":[{"url":"192.168.122.181:8084","publicUrl":"192.168.122.181:8084"},{"url":"192.168.122.181:8083","publicUrl":"192.168.122.181:8083"}]}
~~~

第二步，　根据获得的volume服务的url，下载文件。　由于我上传的图片，所以我直接在浏览器中访问。 文件url格式为 url + '/' + fid. 也支持其它更多的url格式，请查看官方文档。 

前一步中返回的二个volume服务器地址，因此在浏览器中，输入下面任意一个地址，都能打开我刚上传的图片。 用curl也可下载文件。
```
    http://192.168.122.181:8083/2,01d3fecb00 , http://192.168.122.181:8084/2,01d3fecb00
```
