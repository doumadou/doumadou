---
layout: post
title: Mysql自带函数的使用
category: mysql
tags: []
date: 2016-05-31 17:03:44
---

测试表结构:CREATE TABLE aaa (qishu bigint, num1 int, num2 int, timeline TIMESTAMP);

```
mysql> desc aaa;
+----------+------------+------+-----+-------------------+-----------------------------+
| Field    | Type       | Null | Key | Default           | Extra                       |
+----------+------------+------+-----+-------------------+-----------------------------+
| qishu    | bigint(20) | YES  |     | NULL              |                             |
| num1     | int(11)    | YES  |     | NULL              |                             |
| num2     | int(11)    | YES  |     | NULL              |                             |
| timeline | timestamp  | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
+----------+------------+------+-----+-------------------+-----------------------------+

```

1. max()

每插入一条记录，使用某字段的最大值 + 1。
例如:

+----------+------+------+---------------------+
| qishu    | num1 | num2 | timeline            |
+----------+------+------+---------------------+
| 20160522 |    5 |    2 | 2016-05-31 08:58:22 |
| 20160523 |    7 |    7 | 2016-05-31 08:58:53 |
| 20160524 |    6 |    9 | 2016-05-31 08:59:09 |
| 20160525 |    8 |    4 | 2016-05-31 08:59:16 |
| 20160526 |    7 |    4 | 2016-05-31 08:59:21 |
+----------+------+------+---------------------+

有上表，每插入一条记录，　qishu的值都等于最大值＋1;


sql如下:

```
mysql> insert into aaa(qishu, num1, num2) select (select MAX(qishu)+1 from aaa) as max_id, 11, 22;

+----------+------+------+---------------------+
| qishu    | num1 | num2 | timeline            |
+----------+------+------+---------------------+
| 20160522 |    5 |    2 | 2016-05-31 08:58:22 |
| 20160523 |    7 |    7 | 2016-05-31 08:58:53 |
| 20160524 |    6 |    9 | 2016-05-31 08:59:09 |
| 20160525 |    8 |    4 | 2016-05-31 08:59:16 |
| 20160526 |    7 |    4 | 2016-05-31 08:59:21 |
| 20160527 |   11 |   22 | 2016-05-31 09:07:58 |
+----------+------+------+---------------------+
```


2. rand() 随机数

每次插入字段 num1, num2的值随机(0-9)的整数

```
insert into aaa(qishu, num1, num2) select (select MAX(qishu) from aaa) as max_id, cast( floor(rand()*10) as int), cast( floor(rand()*10) as int) from aaa;
```

mysql> select cast( (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CURDATE()) + 60 * 5) / (60 * 5) as int);
+---------------------------------------------------------------------------------------+
| cast( (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CURDATE()) + 60 * 5) / (60 * 5) as int) |
+---------------------------------------------------------------------------------------+
|                                                                                   115 |
+---------------------------------------------------------------------------------------+
1 row in set (0.00 sec)



3. 设置mysql时区

```
mysql> show variables like '%time_zone%';
+------------------+--------+
| Variable_name    | Value  |
+------------------+--------+
| system_time_zone | UTC    |
| time_zone        | SYSTEM |
+------------------+--------+
2 rows in set (0.00 sec)

mysql> set time_zone = '+8:00';
Query OK, 0 rows affected (0.00 sec)

```



CREATE EVENT `course_listener` ON SCHEDULE EVERY 15 SECOND STARTS '2016-05-31 17:45:00' ON COMPLETION PRESERVE ENABLE DO insert into aaa(qishu, num1, num2) select (select CONCAT(date(now()) - 0, cast( (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CURDATE()) + 60 * 5) / (60 * 5) as int))) as max_id, cast( floor(rand()*10) as int), cast( floor(rand()*10) as int);


CREATE EVENT `course_listener` ON SCHEDULE EVERY 15 SECOND STARTS '2016-05-31 17:45:00' ON COMPLETION PRESERVE ENABLE DO insert ignore into aaa(qishu, num1, num2) select ( select CONCAT(date(now()) - 0, right(CONCAT("000", cast( (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(CURDATE()) + 60*2.5) / (60 * 5) as int)),3))) as max_id, cast( floor(rand()*10) as int), cast( floor(rand()*10) as int);

