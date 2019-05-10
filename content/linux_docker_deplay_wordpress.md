---
layout: post
title: 使用docker 部署wordpress
category: wordpress
tags: [wordpress, docker, mysql]
date: 2019-05-10 11:04:02
---

启动mysql
# docker run --name mysql-wordpress -d -v /root/mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD="mysqlpassword" mysql

启动wordpress
# docker run --name wordpress -d -p 80:80 --link mysql-wordpress:mysql -v /root/wordpress-html:/var/www/html wordpress


如果备份： 备份/root/mysql-data 和 /root/wordpress-html二个文件夹即可


出错，即解决方法:

打开网站，出现"Error establishing a database connection" 无法连接到数据的提示。查看wordpress容器的日志

# docker logs wordpress

出现: "The server requested authentication method unknown to the client "

解决方法： 连接mysql，执行如下命令

```
use mysql
ALTER USER 'root' IDENTIFIED WITH 'mysql_native_password' BY 'mysqlpassword';
```


具体执行过程如下:
```
# docker exec -it mysql-wordpress /bin/bash
root@8bf025f7e6da:/# mysql -u root -p 
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 31
Server version: 8.0.14 MySQL Community Server - GPL

Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> ALTER USER 'root' IDENTIFIED WITH 'mysql_native_password' BY 'woyaoxuehuilinux';
Query OK, 0 rows affected (0.01 sec)

```
