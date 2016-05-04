---
layout: post
title: sql直接修改mysql dede表中的数据
category: mysql
tags: [mysql, sql, dede]
date: 2016-05-05 00:25:16
---


场景:修改dede网站后台部分栏目的英文名称, 保存目录. 


由于汲及到的修改的栏目比较多, 而且都是有规律的修改, 因此直接通过sql修改数据库. 这样最为快速,方便.

原数据如下:

```
mysql> select typedir,typenamedir,typename from dede_arctype where topid=50 and reid!=topid;
+-----------------------+-------------+------------------------+
| typedir               | typenamedir | typename               |
+-----------------------+-------------+------------------------+
| /xinjiapoVPS_yunzhuji | sgcloud     | 新加坡VPS/云主机       |
| /taiguoVPS_yunzhuji   | thcloud     | 泰国VPS/云主机         |
| /yuenanVPS_yunzhuji   | vncloud     | 越南VPS/云主机         |
| /malaixiyaVPS         | mycloud     | 马来西亚VPS租用        |
| /jpcloud              | jpcloud     | 日本VPS/云主机         |
| /hanguoVPS_yunzhuji   | hrcloud     | 韩国VPS/云主机         |
| /yinduVPS_yunzhuji    | incloud     | 印度VPS/云主机         |
| {cmspath}/phcloud     | phcloud     | 菲律宾VPS租用          |
| /hkcloud              | hkcloud     | 香港VPS/云主机         |
| /twcloud              | twcloud     | 台湾VPS/云主机         |
| /deguoVPS_yunzhuji    | decloud     | 德国VPS/云主机         |
| /rucloud              | ru          | 俄罗斯VPS/云主机       |
| /helanVPS_yunzhuji    | nlcloud     | 荷兰VPS/云主机         |
| /yingguoVPS_yunzhuji  | ukcloud     | 英国VPS/云主机         |
| {cmspath}/lvcloud     | lv          | 拉脱维亚VPS            |
| /uscloud              | us          | 美国VPS/云主机         |
| {cmspath}/cacloud     | ca          | 加拿大VPS租用          |
| /brcloud              | br          | 巴西VPS/云主机         |
| /aucloud              | au          | 澳洲VPS/云主机         |
+-----------------------+-------------+------------------------+
19 rows in set (0.00 sec)

```

目标:  将typenamedir字段的cloud去掉. 将typedir字段的内容改为 '/' + typenamedir字段内容 + 'cloude'的字符串. 

第一步去掉cloud字符串, 使用sql 的replace函数.

```
mysql> update dede_arctype set typenamedir = replace(typenamedir,'cloud','') where topid=50 and reid!=topid;
Query OK, 13 rows affected (0.00 sec)
Rows matched: 19  Changed: 13  Warnings: 0
```

第二步更新typedir字段内容, 使用sql的concat函数(MySQL连贯字符串不能利用加号(+)，而利用concat。)

```
mysql> update dede_arctype set typedir = concat('/',typenamedir,'cloud') where topid=50 and reid!=topid;
Query OK, 19 rows affected (0.00 sec)
Rows matched: 19  Changed: 19  Warnings: 0
```


OK, 搞定.


```
mysql> select typedir,typenamedir,typename from dede_arctype where topid=50 and reid!=topid;
+----------+-------------+------------------------+
| typedir  | typenamedir | typename               |
+----------+-------------+------------------------+
| /hkcloud | hk          | 香港VPS/云主机         |
| /sgcloud | sg          | 新加坡VPS/云主机       |
| /thcloud | th          | 泰国VPS/云主机         |
| /vncloud | vn          | 越南VPS/云主机         |
| /mycloud | my          | 马来西亚VPS租用        |
| /jpcloud | jp          | 日本VPS/云主机         |
| /hrcloud | hr          | 韩国VPS/云主机         |
| /twcloud | tw          | 台湾VPS/云主机         |
| /incloud | in          | 印度VPS/云主机         |
| /phcloud | ph          | 菲律宾VPS租用          |
| /decloud | de          | 德国VPS/云主机         |
| /rucloud | ru          | 俄罗斯VPS/云主机       |
| /nlcloud | nl          | 荷兰VPS/云主机         |
| /ukcloud | uk          | 英国VPS/云主机         |
| /lvcloud | lv          | 拉脱维亚VPS            |
| /uscloud | us          | 美国VPS/云主机         |
| /cacloud | ca          | 加拿大VPS租用          |
| /brcloud | br          | 巴西VPS/云主机         |
| /aucloud | au          | 澳洲VPS/云主机         |
+----------+-------------+------------------------+
19 rows in set (0.00 sec)

```
