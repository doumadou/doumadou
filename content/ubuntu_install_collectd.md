---
layout: post
title: ubuntu安装collectd web前端
category: linux
tags: [collectd]
date: 2016-04-11 09:18:44
---

collectd的安装，不多说，很简单，直接按官方文档安装即可。本文说说如果安装collectd图形显示

https://collectd.org/download.shtml#debian

#安装依赖：
~~~
	# apt-get install librrds-perl libconfig-general-perl libhtml-parser-perl  libregexp-common-perl
~~~

# 安装apache

~~~
	# apt-get install apache2 libapache2-mod-perl2
~~~


# 修改web配置项

确保配置项里有
```
     <Directory "/var/www/collection3/bin">
     AllowOverride All 
     Options All    
     Order allow,deny
     Allow from all
    </Directory>

     AddHandler cgi-script .cgi .pl

```
