---
layout: post
title: Mysql交换2个表的表名
category:  mysql
tags: [mysql]
date: 2016-06-27 15:06:31
---

如果将2个表的表名对调。

由于不能影响业务。所以在进行表名修改时，我们必须同时将这二个同进行锁定，以防在改表名的过程中数据写入出错。

```
LOCK TABLES t1 WRITE, t2 WRITE;
ALTER TABLE t1 RENAME TO t3;
ALTER TABLE t2 RENAME TO t1;
LOCK TABLES t3 WRITE;
ALTER TABLE t3 RENAME TO t2;
UNLOCK TABLES;
```

在进行临时表rename的时候，也需对临时表加锁。

如果版本比较新一点的Mysql，rename表身就是原子操作，而且支持同时修改多个表的名称，因此我们可以按如下命令操作。

```
rename table t1 to t3, t2 to t1, t3 to t2;
```

有没有很方便^-^。
