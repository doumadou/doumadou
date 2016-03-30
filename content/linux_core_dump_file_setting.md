---
layout: post
title: linux设置程序core dump
category: linux
tags: [linux, core dump]
date: 2016-03-30 09:35:52
---


1.  sysctl -w kernel.core_pattern=/tmp/core-%e-%p

2.  ulimit -c unlimited

查看:
~~~
	# sysctl -a |grep core
	kernel.core_pattern = /tmp/core-%e-%p
~~~

