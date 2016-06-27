---
layout: post
title: mysql/mysqladmin指定配置文件仍然报错
category: mysql
tags: [mysql, mysql错误]
date: 2016-06-27 16:22:00
---

现象：
```
[root@a71641d705a7 mysql-5.6.31-linux-glibc2.5-x86_64]# ./bin/mysql --defaults-file=./my.cnf -u root password 'root'      
./bin/mysqladmin: connect to server at 'localhost' failed
error: 'Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)'
Check that mysqld is running and that the socket: '/tmp/mysql.sock' exists!

[root@a71641d705a7 mysql-5.6.31-linux-glibc2.5-x86_64]# ./bin/mysqladmin --defaults-file=./my.cnf -u root password 'root'      
./bin/mysqladmin: connect to server at 'localhost' failed
error: 'Can't connect to local MySQL server through socket '/tmp/mysql.sock' (2)'
Check that mysqld is running and that the socket: '/tmp/mysql.sock' exists!
```

解决方法:

* 查看mysqld 的sock文件，然后建立软连接。

* 修改my.cnf, 加入client的socket项。
```
[client]
socket=/opt/mysql/mysql.sock 
```
