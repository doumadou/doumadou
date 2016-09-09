---
layout: post
title: Centos7 x86_64编译msitools
category: linux
tags: [linux, msitools]
date: 2016-09-09 16:04:56
---




下载gcab相关的二个RPM包

```
# wget http://download.opensuse.org/repositories/windows:/mingw/openSUSE_Factory/x86_64/gcab-devel-0.7-21.7.x86_64.rpm
# wget http://download.opensuse.org/repositories/windows:/mingw/openSUSE_Factory/x86_64/libgcab-1_0-0-0.7-21.7.x86_64.rpm
# rpm -vih gcab-devel-0.7-21.7.x86_64.rpm libgcab-1_0-0-0.7-21.7.x86_64.rpm 
```

安装依赖

```
# yum install -y glib2-devel libgsf-devel libuuid-devel
```


编译安装

```
# wget http://ftp.gnome.org/pub/GNOME/sources/msitools/0.95/msitools-0.95.tar.xz
# tar vxf msitools-0.95.tar.xz
# cd msitools-0.95
# 注释GOBJECT_INTROSPECTION_CHECK这一样，要不然会出错
# sed -i "s/GOBJECT_INTROSPECTION_CHECK/#GOBJECT_INTROSPECTION_CHECK/g" configure.ac
# sh autogen.sh 
# make
# make install
```
