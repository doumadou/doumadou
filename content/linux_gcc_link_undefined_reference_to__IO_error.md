---
layout: post
title: undefined reference to `_IO出错原因及解决方法
category: c/c++
tags: [linux, c]
date: 2016-03-30 09:37:08
---


编译程序时出现：

undefined reference to `_IO


原因：这个错误由ioctl调用引起的。


解决方法: 加入ioctl对应的头文件即可。(#include <sys/ioctl.h>)
