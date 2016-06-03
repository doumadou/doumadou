---
layout: post
title: Mysql
category: 
tags: [mysql]
date: 2016-06-01 15:53:16
---

# Mysql 介绍

# 实验环境介绐

docker + centos7.1 + mariadb 5.5

# mysql安装使用

## mysql源码安装
## mysql源码目录介绐

## mysql 相关命令解读
* mysql_install_db: 初始化mysql数据文件及创建系统表
```
# mysql_install_db --user=mysql
[root@442e288e8456 /]# ls -ltr /var/lib/mysql/
total 32
drwx------ 2 mysql root   4096 Jun  3 01:24 test
drwx------ 2 mysql root   4096 Jun  3 01:24 mysql
drwx------ 2 mysql mysql  4096 Jun  3 01:24 performance_schema
-rw-rw---- 1 mysql mysql    52 Jun  3 01:24 aria_log_control
-rw-rw---- 1 mysql mysql 16384 Jun  3 01:24 aria_log.00000001
```
* mysqld_safe : 推荐启动mysql server的方式，在启动mysql时加入了一些安全特性,监控mysql的运行状况. 例如当发生错误时，mysqld会重启。
```
# mysqld_safe &
```

* mysqladmin:  mysql管理操作的客户端，通过它可以检查服务器的配置，当前运行状态，创建删除数据库，初始化root密码等。

设置 root 密码 
```
# /usr/bin/mysqladmin -u root password 'root'
```

关闭mysql服务
```
# mysqladmin -u root -proot shutdown

```

## mysql 配置文件my.cnf

## Mysql 数据文件

## mysql 多实例


# 二进制日志

配置项(my.cnf)
log_bin=/tmp/mysql-bin #默认无此项，表示binlog 没有开启，加入此项即开启binlog.  服务启动后将生成如下这些文件

```
[root@442e288e8456 /]# ls -ltr /tmp/mysql-bin.*
-rw-rw---- 1 mysql mysql 245 Jun  3 01:41 /tmp/mysql-bin.000001
-rw-rw---- 1 mysql mysql  22 Jun  3 01:41 /tmp/mysql-bin.index
```

.index : 文件里记录了有哪些binlog文件 
.0000*: 真实的binlog文件，使用mysqlbinlog /tmp/mysql-bin.000001 可输出成sql格式的内容。

## 管理二进制日志

* 查看二进制日志是否打开
```
MariaDB [(none)]> show variables like '%log_bin%';
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin                         | ON    |
| log_bin_trust_function_creators | OFF   |
| sql_log_bin                     | ON    |
+---------------------------------+-------+
3 rows in set (0.00 sec)

```
* 查看二进制日志文件情况
```
MariaDB [(none)]> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |       245 |
+------------------+-----------+
1 row in set (0.00 sec)

MariaDB [(none)]> show master logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql-bin.000001 |       245 |
+------------------+-----------+
1 row in set (0.00 sec)

```

#　查询日志
查询日志文件记录所有客户端发来的SQL语句
通过general_log参数配置

* 打开查询日志功能
```
MariaDB [(none)]> show variables like '%log';
+----------------------------------+-------+
| Variable_name                    | Value |
+----------------------------------+-------+
| back_log                         | 50    |
| general_log                      | OFF   |
| innodb_locks_unsafe_for_binlog   | OFF   |
| innodb_recovery_update_relay_log | OFF   |
| log                              | OFF   |
| relay_log                        |       |
| slow_query_log                   | OFF   |
| sync_binlog                      | 0     |
| sync_relay_log                   | 0     |
+----------------------------------+-------+
9 rows in set (0.00 sec)
MariaDB [(none)]> set global general_log=1;
Query OK, 0 rows affected (0.00 sec)

MariaDB [(none)]> show variables like '%log';
+----------------------------------+-------+
| Variable_name                    | Value |
+----------------------------------+-------+
| back_log                         | 50    |
| general_log                      | ON    |
| innodb_locks_unsafe_for_binlog   | OFF   |
| innodb_recovery_update_relay_log | OFF   |
| log                              | ON    |
| relay_log                        |       |
| slow_query_log                   | OFF   |
| sync_binlog                      | 0     |
| sync_relay_log                   | 0     |
+----------------------------------+-------+
9 rows in set (0.00 sec)
```

set global general_log=1, 同时会将log 设为on

* 查看文件位置
```
MariaDB [(none)]> show variables like '%file';
+-------------------------+------------------------------+
| Variable_name           | Value                        |
+-------------------------+------------------------------+
| ft_stopword_file        | (built-in)                   |
| general_log_file        | 442e288e8456.log             |
| init_file               |                              |
| innodb_doublewrite_file |                              |
| local_infile            | ON                           |
| pid_file                | /var/run/mariadb/mariadb.pid |
| relay_log_info_file     | relay-log.info               |
| slow_query_log_file     | 442e288e8456-slow.log        |
+-------------------------+------------------------------+
8 rows in set (0.00 sec)
```

如果Value的值非绝对路径，则表示文件位于mysql数据文件的相对目录下。

查询日志也可通过my.cnf文件配置
```
general_log=1
general_log_file=/tmp/query_log.log
```

查看日志内容
```
[root@442e288e8456 mysql]# cat 442e288e8456.log 
/usr/libexec/mysqld, Version: 5.5.47-MariaDB-log (MariaDB Server). started with:
Tcp port: 3306  Unix socket: /var/lib/mysql/mysql.sock
Time                 Id Command    Argument
160603  2:55:18	    1 Query	show variables like '%log'
160603  2:56:05	    1 Query	shwo variables like '%file'
160603  2:56:09	    1 Query	show variables like '%file'
160603  2:57:41	    1 Query	ls
160603  2:58:03	    1 Query	show databases
160603  2:58:16	    1 Query	create database test_bin_log
160603  2:58:21	    1 Query	SELECT DATABASE()
		    1 Init DB	test_bin_log
		    1 Query	show databases
		    1 Query	show tables
160603  2:58:48	    1 Query	create table a(id int primary key, num1 int, num2 int)
160603  2:58:56	    1 Query	insert into a(0, 1, 2)
160603  2:59:07	    1 Query	insert into a values(0, 1, 2)
160603  2:59:12	    1 Query	select * from a
```


# 慢查询

* 打开慢查询日志功能
```
MariaDB [test_bin_log]> show variables like 'slow%';
+---------------------+-----------------------+
| Variable_name       | Value                 |
+---------------------+-----------------------+
| slow_launch_time    | 2                     |
| slow_query_log      | OFF                   |
| slow_query_log_file | 442e288e8456-slow.log |
+---------------------+-----------------------+
3 rows in set (0.00 sec)

MariaDB [test_bin_log]> set global slow_query_log=1;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test_bin_log]> show variables like 'slow%';
+---------------------+-----------------------+
| Variable_name       | Value                 |
+---------------------+-----------------------+
| slow_launch_time    | 2                     |
| slow_query_log      | ON                    |
| slow_query_log_file | 442e288e8456-slow.log |
+---------------------+-----------------------+
3 rows in set (0.00 sec)

MariaDB [test_bin_log]> system cat /var/lib/mysql/442e288e8456-slow.log
/usr/libexec/mysqld, Version: 5.5.47-MariaDB-log (MariaDB Server). started with:
Tcp port: 3306  Unix socket: /var/lib/mysql/mysql.sock
Time                 Id Command    Argument
MariaDB [test_bin_log]> 
```

* 慢查询相关参数配置
1) long_query_time:  当查询超时long_query_time 指定时间(单位 s)，则记录到慢查询日志，默认为10s
```
MariaDB [test_bin_log]> show variables like 'long%';
+-----------------+-----------+
| Variable_name   | Value     |
+-----------------+-----------+
| long_query_time | 10.000000 |
+-----------------+-----------+
1 row in set (0.01 sec)

MariaDB [test_bin_log]> set session long_query_time=1;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test_bin_log]> show variables like 'long%';
+-----------------+----------+
| Variable_name   | Value    |
+-----------------+----------+
| long_query_time | 1.000000 |
+-----------------+----------+
1 row in set (0.00 sec)

```

相关测试:
```
MariaDB [test_bin_log]> create table t as select * from information_schema.tables;
Query OK, 105 rows affected (0.10 sec)
Records: 105  Duplicates: 0  Warnings: 0

重复多步后，执行时间达到1.04 sec, 所以记录到慢查询日志中。
MariaDB [test_bin_log]> insert into t select * from t;
Query OK, 26880 rows affected (1.04 sec)
Records: 26880  Duplicates: 0  Warnings: 0

MariaDB [test_bin_log]> system cat /var/lib/mysql/442e288e8456-slow.log
/usr/libexec/mysqld, Version: 5.5.47-MariaDB-log (MariaDB Server). started with:
Tcp port: 3306  Unix socket: /var/lib/mysql/mysql.sock
Time                 Id Command    Argument
# Time: 160603  5:47:51
# User@Host: root[root] @ localhost []
# Thread_id: 1  Schema: test_bin_log  QC_hit: No
# Query_time: 1.050285  Lock_time: 0.000105  Rows_sent: 0  Rows_examined: 53760
use test_bin_log;
SET timestamp=1464932871;
insert into t select * from t;

```

* log_queries_not_using_indexes:  当为ON时，如果执行一个sql语句，如果这个表没有索引则表这个SQL记录到慢查询文件

```
MariaDB [test_bin_log]> show variables like "%not_using%";
+-------------------------------+-------+
| Variable_name                 | Value |
+-------------------------------+-------+
| log_queries_not_using_indexes | OFF   |
+-------------------------------+-------+
1 row in set (0.00 sec)

MariaDB [test_bin_log]> set global log_queries_not_using_indexes=1;
Query OK, 0 rows affected (0.00 sec)

MariaDB [test_bin_log]> show variables like "%not_using%";
+-------------------------------+-------+
| Variable_name                 | Value |
+-------------------------------+-------+
| log_queries_not_using_indexes | ON    |
+-------------------------------+-------+
1 row in set (0.00 sec)
```

测试:
```
MariaDB [test_bin_log]> show index from t;
Empty set (0.00 sec)

MariaDB [test_bin_log]> select * from t where TABLE_NAME=")))))))))))))";
Empty set (0.08 sec)

MariaDB [test_bin_log]> system cat /var/lib/mysql/442e288e8456-slow.log
/usr/libexec/mysqld, Version: 5.5.47-MariaDB-log (MariaDB Server). started with:
Tcp port: 3306  Unix socket: /var/lib/mysql/mysql.sock
Time                 Id Command    Argument
# Time: 160603  5:47:51
# User@Host: root[root] @ localhost []
# Thread_id: 1  Schema: test_bin_log  QC_hit: No
# Query_time: 1.050285  Lock_time: 0.000105  Rows_sent: 0  Rows_examined: 53760
use test_bin_log;
SET timestamp=1464932871;
insert into t select * from t;
# Time: 160603  5:58:03
# User@Host: root[root] @ localhost []
# Thread_id: 1  Schema: test_bin_log  QC_hit: No
# Query_time: 0.083622  Lock_time: 0.000109  Rows_sent: 0  Rows_examined: 53760
SET timestamp=1464933483;
select * from t where TABLE_NAME=")))))))))))))";
```


查询日志也可通过my.cnf文件配置
```
slow_query_log=1
slow_query_log_file=/tmp/slow_query_log.log
```


# MYIASM
# Innodb
## undo/redo log 日志原理

### redolog

先介绍几个相关名词(bufferpool, dirtypage, checkpoint, LSN)
Innodb的事务日志是指Redo log，简称Log,保存在日志文件ib_logfile*里面。Innodb还有另外一个日志Undo log，但Undo log是存放在共享表空间里面的（ibdata*文件）。

由于Log和Checkpoint紧密相关，因此将这两部分合在一起分析。

名词解释：LSN，日志序列号，Innodb的日志序列号是一个64位的整型。 

#### 写入机制
* Log写入
**LSN实际上对应日志文件的偏移量**，新的LSN＝旧的LSN + 写入的日志大小。举例如下：
LSN＝1G，日志文件大小总共为600M，本次写入512字节，则实际写入操作为：
l 求出偏移量：由于LSN数值远大于日志文件大小，因此通过取余方式，得到偏移量为400M；
l 写入日志：找到偏移400M的位置，写入512字节日志内容，下一个事务的LSN就是1000000512； 

* checkpoint 写入
**Innodb实现了Fuzzy Checkpoint的机制**，每次取到最老的脏页，然后确保此脏页对应的LSN之前的LSN都已经写入日志文件，再将此脏页的LSN作为Checkpoint点记录到日志文件，意思就是“此LSN之前的LSN对应的日志和数据都已经写入磁盘文件”。恢复数据文件的时候，Innodb扫描日志文件，当发现LSN小于Checkpoint对应的LSN，就认为恢复已经完成。

Checkpoint写入的位置在日志文件开头固定的偏移量处，即每次写Checkpoint都覆盖之前的Checkpoint信息。

#### 保护机制


* 当事务需要修改某条记录时， InnoDB需要将该数据所在的page从disk读到bufferpool中， 事务提交后，InnoDB修改page中的记录。这时bufferpool中的page就和disk中的数据不一致了。我们称bufferpool中的page为dirtypage. Dirtypage等待flush到disk

Dirtypage何时flush到disk上:
1) 当检测到系统空闭时，会flush， 每次64pages.


# Mysql体系结构

# 用户管理
# mysqldump备份数据库

# 数据库备份与恢复

# 数据主从同步
## 同步原理

#实例:  mysql + lvs + keeplived实现读操作负载均衡

# 数据库事务

查看数库的大小

mysql> select table_schema as 'Db Name', Round(Sum(data_length + index_length) / 1024 / 1024, 3) as 'Db Size (MB)', Round(Sum(data_free) / 1024 / 1024, 3) as 'Free Space (MB)' from information_schema.tables group by table_schema;
+--------------------+--------------+-----------------+
| Db Name            | Db Size (MB) | Free Space (MB) |
+--------------------+--------------+-----------------+
| information_schema |        0.172 |           0.000 |
| mysql              |        5.683 |           0.001 |
| performance_schema |        0.000 |           0.000 |
| test               |        0.031 |           0.000 |
| wordpress          |        2.109 |           4.000 |
+--------------------+--------------+-----------------+
5 rows in set (0.01 sec)



# Mysql优化原则
## sql语句的优化
* 避免全表扫描的语句
* 首先考虑在where子句及order by子句上建立索引
* 每条sql最多只会走一条索引
* 建立过多的索引会带插入和更新时开销
* 对于区分度不大的字段，就避免建立索引

* 尽量使用exists/not exists 代替in, not in； 因为后者很有可能会导致全表扫描而放弃索引
* 尽量避免在where子句中对子段进行NULL判断，因为NULL判断会导致全表扫描
* 尽量避免在where子句中使用or作为连接条件, 同样也会导致全局扫描
* 尽量避免在where子句中使用!= 或 <> 操作符, 同样也会导致全局扫描
* 尽量避免在Where子句中使用表达式操作符, 因为同样会导致全表扫描
* 尽量避免在Where子句中对字段使用函数, 因为同样会导致全表扫描
* Select语句中尽量 避免使用“*”，因为在SQL语句在解析的过程中，会将“*”转换成所有列的列名，而这个工作是通过查询数据字典完成的，有一定的开销；
* 使用like "%like%" 或 like "%like" 也同样会导致全局描述，而 like "like%" 会使用索引
* Where子句中，表连接条件应该写在其他条件之前，因为Where子句的解析是从后向前的，所以尽量把能够过滤到多数记录的限制条件放在Where子句的末尾；
* 在使用Union操作符时，应该考虑是否可以使用Union ALL来代替，因为Union操作符在进行结果合并时，会对产生的结果进行排序运算，删除重复记录，对于没有该需求的应用应使用Union ALL，后者仅仅只是将结果合并返回，能大幅度提高性能；
* 若数据库表上存在诸如index(a,b,c)之类的联合索引，则Where子句中条件字段的出现顺序应该与索引字段的出现顺序一致，否则将无法使用该联合索引；
* From子句中表的出现顺序同样会对SQL语句的执行性能造成影响，From子句在解析时是从后向前的，即写在末尾的表将被优先处理，应该选择记录较少的表作为基表放在后面，同时如果出现3个及3个以上的表连接查询时，应该将交叉表作为基表；

* 尽量使用>=操作符代替>操作符，例如，如下SQL语句，select dbInstanceIdentifier  from DBInstance where id > 3，该语句应该替换成 select dbInstanceIdentifier from DBInstance where id >=4 ，两个语句的执行结果是一样的，但是性能却不同，后者更加 高效，因为前者在执行时，首先会去找等于3的记录，然后向前扫描，而后者直接定位到等于4的记录。

  explain 可用于优化分析
## 数据表结构的优化
   表结构优化主要指正确建立索引
如何正确的建立索引，因为不合理的建立索引会导致查询全表扫描，同时过多的索引会带来插入与更新的开销 

* 首先要明确每一条SQL语句最多只可能使用一个索引，如果出现多个可以使用的索引，系统会根据执行代价，选择一个索引执行
* 对于区分度不带的字段，不要建立索引
* 对于Innodb表，虽然如果用户不指定主键，系统会自动生成一个主键列，但是自动产生的主键列有多个问题1. 性能不足，无法使用cache读取；2. 并发不足，系统所有无主键表，共用一个全局的Auto_Increment列。因此，InnoDB的所有表，在建表同时必须指定主键
* 一个字段只需建一种索引即可，无需建立了唯一索引，又建立INDEX索引
* 对于大的文本字段或者BLOB字段，不要建立索引；
* 连接查询的连接字段应该建立索引；
* 排序字段一般要建立索引；
* 分组统计字段一般要建立索引；
* 正确使用联合索引，联合索引的第一个字段是可以被单独使用的，例如有如下联合索引index(userID,dbInstanceID),一下查询语句是可以使用该索引的，select dbInstanceIdentifier from DBInstance where userID=? ，但是语句select dbInstanceIdentifier from DBInstance where dbInstanceID=?就不可以使用该索引；
* 索引一般用于记录比较多的表，假如有表DBInstance，所有查询都有userID条件字段，目前已知该字段已经能够很好的区分记录，即每一个userID下记录数量不多，所以该表只需在userID上建立一个索引即可，即使有使用其他条件字段，由于每一个userID对应的记录数据不多，所以其他字段使用不用索引基本无影响，同时也可以避免建立过多的索引带来的插入和更新的性能开销；


## 服务器配置的优化

配置优化主要指Mysql参数优化
1）MySQL服务器有慢连接日志，可以将超过一定时间间隔和不使用索引的查询语句记录下来方便开发人员跟踪，可以通过设置slow_query_log=ON/OFF打开和关闭慢连接日志功能，slow_query_log_file设置慢连接日志的文件名，long_query_time设置超时时间，单位是ms,注意慢连接日志MySQL默认是关闭的；

2）MySQL有查询缓存的功能，服务器会保存查询语句和相应的返回结果来减少相同的查询造成的服务器开销，可以通过设置query_cache_size设置查询缓存的大小，0表示关闭查询缓存，但是值得注意的是，一旦该表有更新，则所有的查询缓存都会失效，默认情况下，MySQL是关闭查询缓存的；

3）可以通过配置max_connections设置数据库的最大连接数，wait_timeout设置连接最长保留时间，该时间单位是s, MySQL默认是8个小时，一旦超过8个小时，数据库会自动断开该连接，这点在使用数据库连接池时由为需要注意，因为连接池中的连接可能已经被服务器断开了，到那时连接池不知道，应用在从连接池中获取到该连接使用时就会出错，max_connect_errors配置如果应用出现多次异常，则会终止主机连接数据库；
