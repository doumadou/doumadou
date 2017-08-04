---
layout: post
title: php 500 It is not safe to rely on the system 出错
category: php
tags: []
date: 2017-08-04 17:43:58
---

 It is not safe to rely on the system解决方法,其实就是时区设置不正确造成的,本文提供了3种方法来解决这个问题。
实际上，从PHP 5.1.0开始当对使用date()等函数时，如果timezone设置不正确，在每一次调用时间函数时，都会产生E_NOTICE 或者 E_WARNING 信息，而又在php中，date.timezone这个选项，默认情况下是关闭的，无论用什么php命令都是格林威治标准时间，但是PHP5.3中如果没有设置部分时间类函数也会强行抛出了这个错误的。
PS:现在由于大部分人使用VPS/云主机，需要自己配置的环境的就更加会容易出现这个情况。

Error message:
```
PHP message: An exception has been thrown during the rendering of a template ("strtotime(): It is not safe to rely on the system's timezone settings. You are *required* to use the date.timezone setting or the date_default_timezone_set() function. In case you used any of those methods and you are still getting this warning, you most likely misspelled the timezone identifier. We selected 'America/New_York' for 'EDT/-4.0/DST' instead") in "search.html" at line 76" while reading response header from upstream, client: 192.168.231.218, server: www.*****.com, request: "GET /sea-first-asc-1 HTTP/1.1", upstream: "fastcgi://unix:/var/run/php5-fpm.sock:", host: "www.****.com", referrer: "http://www.****.com/"
```

解决方案:

1. 修改时区。
```
# cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
```

2.
在php.ini里加上找到date.timezone项，设置date.timezone = "Asia/Shanghai"，重启环境就ok了 
