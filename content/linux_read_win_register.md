---
layout: post
title: Linux读取Windows的注册表
category: linux
tags: [windows注册表]
date: 2016-05-27 17:21:38
---

工作中使用libguest修改windows的管理员密码有时会出现修改不成功的情况，于是经过一翻研究，终于解决了这个问题。


其间也研究过windows注册表文件的解析，在此分享一下Linux读取windows注册表信息。


读取注册表信息，只需安装dumphive，即可解析windows注册表文件

dumphive的下载地址为http://gitorious.com/canaima-gnu-linux/dumphive/commits/upstream

或http://bazaar.launchpad.net/~guadalinex-members/dumphive/trunk/revision/1?start_revid=1

使用步骤如下:

1. 安装依赖

dumphive使用由Pascal语言写出的，所以要下载free Pascal的编译器，在Ubuntu下，用apt-get install fpc即可

2. 编译

解压进入src目录。直接make

3. 获取注册表文件, 假设为SYSTEM;解析
```
# ./dumphive /tmp/SYSTEM /tmp/system.reg
```

命令执行完后，/tmp/system.reg就是一直文本文件，直接打开就能看懂了。

注: windows2008的注册表文件位于 c:\\Windows\\System32\\config\\SYSTEM


centos安装:

https://www.freepascal.org/down/x86_64/linux.var 进入http://sourceforge.net/projects/freepascal/files/Linux/3.0.2 下载rpm包

[root@10 taoxie]# rpm -ivh fpc-3.0.2-1.x86_64.rpm 
Preparing...                          ################################# [100%]
Updating / installing...
   1:fpc-3.0.2-1                      ################################# [100%]
Running on linux
Write permission in /etc.
Writing sample configuration file to /etc/fpc.cfg
Writing sample configuration file to /usr/lib64/fpc/3.0.2/ide/text/fp.cfg
Writing sample configuration file to /usr/lib64/fpc/3.0.2/ide/text/fp.ini
Writing sample configuration file to /etc/fppkg.cfg
Writing sample configuration file to /etc/fppkg/default
`
