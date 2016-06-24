---
layout: post
title: Mysql
category: 
tags: [mysql]
date: 2016-06-01 15:53:16
---

# Mysql 介绍


大体上说，数据库主要用于客户端进行DML操作，select用于查询数据，insert/update/delete用于插入/修改/删除数据，根据两类操作的比重不同，数据库可以分为两类：

OLTP型：insert/update/delete 操作多于select

OLAP型：select操作多于insert/update/delete

 

        OLTP是事务型，是增删改比较多，事务小但数量多；OLAP是分析型的，查询比较多，查询数量少但运行时间通常较长。

        对于分析性能问题时，对于把握数据库的主要操作进行归类比较重要，这样可以面对整个业务模型进行归类，化整为零，同时这点也要与上面的业务系统结合，只有了解和熟悉业务状态，才可以在数据库层面运维更好；

        总之，感性认识就是指一个数据库是事务比较多，还是查询比较多。

# 名词解释
* DBMS: 数据库管理系统(Database Management System)
* DML（data manipulation language）：
       它们是SELECT、UPDATE、INSERT、DELETE，就象它的名字一样，这4条命令是用来对数据库里的数据进行操作的语言
* DDL（data definition language）：
       DDL比DML要多，主要的命令有CREATE、ALTER、DROP等，DDL主要是用在定义或改变表（TABLE）的结构，数据类型，表之间的链接和约束等初始化工作上，他们大多在建立表时使用
* DCL（Data Control Language）：
       是数据库控制功能。是用来设置或更改数据库用户或角色权限的语句，包括（grant,deny,revoke等）语句。在默认状态下，只有sysadmin,dbcreator,db_owner或db_securityadmin等人员才有权力执行DCL

# 实验环境介绐

docker + centos7.1 + mariadb 5.5

# mysql安装使用

## mysql源码安装
## mysql源码目录介绐

## 默认数据库介绍
mysql初始化数据文件后，会自动创建如下3个数据库。
mysql;information_schema; performance_schema;
information_schema: 保存着关于MySQL服务器所维护的所有其他数据库的信息。如数据库名，数据库的表，表栏的数据类型与访问权限等。
简单地说，performance_schema数据库与PERFORMANCE_SCHEMA存储引擎一起实现mysql的Performance Schema，也就是mysql的性能监测机制。

下面根据官方手册，给出Performance Schema这种性能监测机制的详细介绍。

MySQL的Performance Schema是用来监测MySQL服务器执行功能的。它有以下特点：

    Performance Schema提供了一种在运行时检查服务器内部执行的方式。它是通过使用PERFORMANCE_SCHEMA存储引擎和performance_schema数据库来实现的。它主要侧重于数据库的性能数据。这是不同于用于元数据检验的INFORMATION_SCHEMA的地方。
    监视服务器事件。


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
* mysqlhotcopy: 快速热备MYISAM引擎的工具(仅支持myisam). 
1、前者是一个快速文件意义上的COPY，后者是一个数据库端的SQL语句集合。
2、前者只能运行在数据库目录所在的机器上，后者可以用在远程客户端。
3、相同的地方都是在线执行LOCK TABLES 以及 UNLOCK TABLES
4、前者恢复只需要COPY备份文件到源目录覆盖即可，后者需要倒入SQL文件到原来库中。(source 或者\.或者 mysql < 备份文件)

设置 root 密码 
```
# /usr/bin/mysqladmin -u root password 'root'
```

关闭mysql服务
```
# mysqladmin -u root -proot shutdown

```

## mysql 配置参数

binlog_cache_size: 为每个session 分配的内存，在事务过程中用来存储二进制日志的缓存。 可以提高bin-log的效率


## Mysql 数据文件
   *.frm是描述了表的结构，*.MYD保存了表的数据记录，*.MYI则是表的索引

innodb:
    ibdata1:默认表空间文件，如果没有设置innodb_file_per_table，则所有的表都是共用同一个文件的。如果启动了innodb_file_per_table，每张表的索引、数据和插入缓冲BITMAP信息是按照表分别独立存放在不同的文件中，但是undo log等其他信息还是存放在默认表空间中。
	*.idb: 当设置innodb_file_per_table时，每个表的表空间文件. 表文件，存放每张表的数据、索引和插入缓冲。
	ib_logfile0: 重做日志文件，备份前记录的LSN和备份结束时的LSN之间的redo log xtrabackup是需要保存的，用于在恢复时进行回放或者回滚。

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

## 二进制日志格式
Mysql binlog日志有三种格式，分别为Statement,MiXED,以及ROW！, 默认为Statement, 推荐使用MiXED.
配置项(my.cnf)
binlog_format           = MIXED                 //binlog日志格式
1.Statement：每一条会修改数据的sql都会记录在binlog中。

优点：不需要记录每一行的变化，减少了binlog日志量，节约了IO，提高性能。(相比row能节约多少性能与日志量，这个取决于应用的SQL情况，正常同一条记录修改或者插入row格式所产生的日志量还小于Statement产生的日志量，但是考虑到如果带条件的update操作，以及整表删除，alter表等操作，ROW格式会产生大量日志，因此在考虑是否使用ROW格式日志时应该跟据应用的实际情况，其所产生的日志量会增加多少，以及带来的IO性能问题。)

缺点：由于记录的只是执行语句，为了这些语句能在slave上正确运行，因此还必须记录每条语句在执行的时候的一些相关信息，以保证所有语句能在slave得到和在master端执行时候相同 的结果。另外mysql 的复制,像一些特定函数功能，slave可与master上要保持一致会有很多相关问题(如sleep()函数， last_insert_id()，以及user-defined functions(udf)会出现问题).

使用以下函数的语句也无法被复制：

* LOAD_FILE()

* UUID()

* USER()

* FOUND_ROWS()

* SYSDATE() (除非启动时启用了 --sysdate-is-now 选项)

同时在INSERT ...SELECT 会产生比 RBR 更多的行级锁

2.Row:不记录sql语句上下文相关信息，仅保存哪条记录被修改。

优点： binlog中可以不记录执行的sql语句的上下文相关的信息，仅需要记录那一条记录被修改成什么了。所以rowlevel的日志内容会非常清楚的记录下每一行数据修改的细节。而且不会出现某些特定情况下的存储过程，或function，以及trigger的调用和触发无法被正确复制的问题

缺点:所有的执行的语句当记录到日志中的时候，都将以每行记录的修改来记录，这样可能会产生大量的日志内容,比如一条update语句，修改多条记录，则binlog中每一条修改都会有记录，这样造成binlog日志量会很大，特别是当执行alter table之类的语句的时候，由于表结构修改，每条记录都发生改变，那么该表每一条记录都会记录到日志中。

3.Mixed: 是以上两种level的混合使用，一般的语句修改使用statment格式保存binlog，如一些函数，statement无法完成主从复制的操作，则采用row格式保存binlog,MySQL会根据执行的每一条具体的sql语句来区分对待记录的日志形式，也就是在Statement和Row之间选择一种.新版本的MySQL中队row level模式也被做了优化，并不是所有的修改都会以row level来记录，像遇到表结构变更的时候就会以statement模式来记录。至于update或者delete等修改数据的语句，还是会记录所有行的变更。


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
## 特点
* 支持事务
* 行级锁
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
* 远程授权访问
```
mysql> GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'root' WITH GRANT OPTION;
```
# mysqldump备份数据库

# 数据库备份与恢复

## mysqldump 逻辑备份
## mysqlhotcopy
## XtraBackup
XtraBackup是Percona公司一款开源的数据库备份软件，相对于mysqldump，它是直接通过拷贝物理文件实现数据库备份的，所以速度相比要快很多。XtraBackup包含两部分：xtrabackup的c程序和innobackupex perl脚本；前者主要用于处理innodb表的备份；后者是前者的封装，主要包括一些与MySQL服务器的通信和mysiam表的备份
* 无锁备份
###实现原理 
基于InnoDB对事务的支持，利用其崩溃恢复的功能来实现的。

# 数据主从同步
## 同步原理

#实例:  mysql + lvs + keeplived实现读操作负载均衡

# 数据库事务
       1.原子性
          组成事务的一组sql命令形成了一个逻辑单元，不能只执行其中的一部分。
      2.一致性
          在事务处理前后，数据库的数据是一致的（数据库的数据完成行约束）。
      3.隔离性
          一个事务处理对另一个事务处理的影响。
      4.持续性
          事务处理的效果能够被永久保留下来 
## 多版本并发控制（MVCC）
## Mysql隔离级别(Isolation)
隔离级别规则了一个事务所做的修改在哪些事务内和事务间是可见的，哪些是不可见的。
下文对隔离级别的说明都是基于锁机制并发控制的数据库管理系统而言的
由ANSI/ISO定义的SQL-92标准定义的四种隔离级别
1.Read Uncommitted
	末提交读，也称为脏读(dirty read). 一个事务可以读到其它事务末提交的更改。
2.Read Committed
	提交读，也称不可重复读。
3.Repeatable Read
    可重复读, 该级别保证同一事务中多次读取同样的记录的结果是一致的。 是mysql默认事务隔离级别
	REPEATABLE READ：在mysql中，不会出现幻读。mysql的实现和标准定义的RR隔离级别有差别。
4.Serializable
	可序列化， 是最高级别的隔离.
	实现可序列化要求在选定的对象上的读锁和写锁保持到事务结束才能释放. 在select 查询中使用一个where子句来描述范围时应获得一个"范围锁(rang-locks)"。这种机制可以避免“幻影读(phantom reads)”现象


事务具有ACID四种特性。

但是Isolation并发可能引起如下问题：

1.脏读

允许读取到未提交的脏数据。

2.不可重复读

如果你在时间点T1读取了一些记录，在T2时再想重新读取一次同样的这些记录时，这些记录可能已经被改变、或者消失不见。

3.幻读

解决了不重复读，保证了同一个事务里，查询的结果都是事务开始时的状态（一致性）。但是，如果另一个事务同时提交了新数据，本事务再更新时，就会“惊奇的”发现了这些新数据，貌似之前读到的数据是“鬼影”一样的幻觉。

隔离解别 	脏读 	不可重复读 	幻读
Read Uncommitted 	Y 	Y 	Y
Read Committed 	N 	Y 	Y
Repeatable(default) 	N 	N 	Y
Serializable 	N 	N 	N



### 查看及修改隔离级别
```
Session 1:
mysql> set global tx_isolation='read-uncommitted';  
Query OK, 0 rows affected (0.00 sec)  
mysql> select @@global.tx_isolation,@@tx_isolation;  
+-----------------------+------------------+  
| @@global.tx_isolation | @@tx_isolation   |  
+-----------------------+------------------+  
| READ-UNCOMMITTED      | READ-UNCOMMITTED |  
+-----------------------+------------------+  
1 row in set (0.00 sec)  
  
Session 2:  
mysql> select @@global.tx_isolation, @@tx_isolation;  
+-----------------------+-----------------+  
| @@global.tx_isolation | @@tx_isolation  |  
+-----------------------+-----------------+  
| READ-UNCOMMITTED      | REPEATABLE-READ |  
+-----------------------+-----------------+  
1 row in set (0.00 sec)  
```

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


# Mysql 性能分析

## explain
```
MariaDB [test]> explain select * from tb1;
+------+-------------+-------+------+---------------+------+---------+------+------+-------+
| id   | select_type | table | type | possible_keys | key  | key_len | ref  | rows | Extra |
+------+-------------+-------+------+---------------+------+---------+------+------+-------+
|    1 | SIMPLE      | tb1   | ALL  | NULL          | NULL | NULL    | NULL |    2 |       |
+------+-------------+-------+------+---------------+------+---------+------+------+-------+
1 row in set (0.00 sec)

MariaDB [test]> explain select * from tb1 where id=1;
+------+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
| id   | select_type | table | type  | possible_keys | key     | key_len | ref   | rows | Extra |
+------+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
|    1 | SIMPLE      | tb1   | const | PRIMARY       | PRIMARY | 4       | const |    1 |       |
+------+-------------+-------+-------+---------------+---------+---------+-------+------+-------+
1 row in set (0.00 sec)

```
各个属性值的含义:

id : select 查询的序列号。
select_type: select查询的类型，主要是区别普通查询和联合查询、子查询之类的复杂查询。
table: 输出的行所引用的表。
type : 联合查询所使用的类型。
type显示的是访问类型，是较为重要的一个指标，结果值从好到坏依次是：
system > const > eq_ref > ref > fulltext > ref_or_null > index_merge > unique_subquery > index_subquery > range > index > ALL
一般来说，得保证查询至少达到range级别，最好能达到ref。
possible_keys: 指写mysql使用哪个索引在表中找到相应的行。 如果是空的，没有相关的索引。这时要提高性能，可通过检验WHERE子句，看是否引用某些字段，或者检查字段不是适合索引。
key:  实际使用的健，若为null, 表示没有索引被选择。
key_len: 显示MySQL决定使用的键长度。如果键是NULL，长度就是NULL。文档提示特别注意这个值可以得出一个多重主键里mysql实际使用了哪一部分。
ref: 显示哪个字段或常数与key一起被使用。
rows : 这个数表示mysql要遍历多少数据才能找到，在innodb上是不准确的。
```
MariaDB [test]> explain select count(*) from tb5;select count(*) from tb5;
+------+-------------+-------+-------+---------------+---------+---------+------+------+-------------+
| id   | select_type | table | type  | possible_keys | key     | key_len | ref  | rows | Extra       |
+------+-------------+-------+-------+---------------+---------+---------+------+------+-------------+
|    1 | SIMPLE      | tb5   | index | NULL          | PRIMARY | 4       | NULL |  904 | Using index |
+------+-------------+-------+-------+---------------+---------+---------+------+------+-------------+
1 row in set (0.00 sec)

+----------+
| count(*) |
+----------+
|     1000 |
+----------+
1 row in set (0.00 sec)

MariaDB [test]> show create table tb5;
+-------+---------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                          |
+-------+---------------------------------------------------------------------------------------------------------------------------------------+
| tb5   | CREATE TABLE `tb5` (
  `id` int(11) NOT NULL,
  `col` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 |
+-------+---------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

```
Extra: 

如果是Only index，这意味着信息只用索引树中的信息检索出的，这比扫描整个表要快。

如果是where used，就是使用上了where限制。

如果是impossible where 表示用不着where，一般就是没查出来啥。

如果此信息显示Using filesort或者Using temporary的话会很吃力，WHERE和ORDER BY的索引经常无法兼顾，如果按照WHERE来确定索引，那么在ORDER BY时，就必然会引起Using filesort，这就要看是先过滤再排序划算，还是先排序再过滤划算。


type=const表示通过索引一次就找到了；
key=primary的话，表示使用了主键；
type=all,表示为全表扫描；
key=null表示没用到索引。type=ref,因为这时认为是多个匹配行，在联合查询中，一般为REF。


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


# 故障解决

## 表误册数据

* )将delete from tb where ? 写成delete from tb;
解决方法，通过bin log 恢复。 
原理： mysqlbinlog
前提： innodb。且mysql开启了bin log日志
