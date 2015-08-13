Title: mysql性能优化分析从零开始---使用PROCEDURE ANALYSE分析表结构
Category: mysql
Tags: mysql, 数据库性能优化
Date: 2015-08-11 17:13:54
---

mysql性能优化分析从0到1, 使用PROCEDURE ANALYSE分析表结构


先从最简单的一张表

mysql> desc filelist;
+-----------+-------------+------+-----+---------+-------+
| Field     | Type        | Null | Key | Default | Extra |
+-----------+-------------+------+-----+---------+-------+
| info_hash | varchar(40) | NO   | PRI | NULL    |       |
| file_list | longtext    | NO   |     | NULL    |       |
+-----------+-------------+------+-----+---------+-------+
2 rows in set (0.02 sec)

简单说明一下。

info_hash： 唯一表示一个资源, 由40个16进制字符组成的字符串表示
file_list： 每个资源所包含的文件信息(文件名，文件大小)。用jion字符串存储. 举个列子: `[{"path": "file1", "length": 10314}, {"path": "file2", "length": 10234}]`

目前表记录数 45000左右

然后通过PROCEDURE ANALYSE分析一下。

mysql> select * from filelist  PROCEDURE ANALYSE(1)\G;
*************************** 1. row ***************************
             Field_name: test_db.filelist.info_hash
              Min_value: 000102652f757cbc70b0db2af8620fb18f7acbd9
              Max_value: ffff1bf66d9ba912935412950c177923dbebb979
             Min_length: 40
             Max_length: 40
       Empties_or_zeros: 0
                  Nulls: 0
Avg_value_or_avg_length: 40.0000
                    Std: NULL
      Optimal_fieldtype: CHAR(40) NOT NULL
*************************** 2. row ***************************
             Field_name: test_db.filelist.file_list
              Min_value: //这里省略，文件太长 
              Max_value: [{"path": "~Get Your Files Here/Men's Health UK.pdf", "length": 33643449}]
             Min_length: 39
             Max_length: 983229
       Empties_or_zeros: 0
                  Nulls: 0
Avg_value_or_avg_length: 2516.2741
                    Std: NULL
      Optimal_fieldtype: MEDIUMTEXT NOT NULL
2 rows in set (2.31 sec)


按建议修改
mysql> ALTER TABLE filelist CHANGE `info_hash` `info_hash` char(40) NOT NULL;  
Query OK, 45315 rows affected (0.84 sec)
Records: 45315  Duplicates: 0  Warnings: 0

[root@localhost mysql]# ls -ltr testdb/
total 137044
-rw-rw---- 1 mysql mysql      8610 Aug 11 04:45 filelist.frm
-rw-rw---- 1 mysql mysql 116317924 Aug 11 04:45 filelist.MYD
-rw-rw---- 1 mysql mysql   3072000 Aug 11 04:45 filelist.MYI
[root@localhost mysql]# ls -ltr /tmp/testdb/
total 136940
-rw-r----- 1 root root      8610 Aug 11 04:38 filelist.frm
-rw-r----- 1 root root 116317924 Aug 11 04:38 filelist.MYD
-rw-r----- 1 root root   2963456 Aug 11 04:38 filelist.MYI


经执行分析后mysql给出的建议

1. info_hash字段改为char(40) NOT NULL

原因分析:
	char与varchar的区别

