---
layout: post
title: linux insmod报错Invalid module format
category: kernel
tags: []
date: 2019-01-16 16:51:21
---

insmod: ERROR: could not insert module ./test.ko: Invalid module format”错误。

用dmesg查到如下信息“no symbol version for module_layout”，

用“find / -name ‘Module.symvers’ ”命令查找Module.symvers文件。发现在/usr/src/kernel/下系统自带的文件夹中有。将该文件cp到/usr/src/kernel/下自己的内核源码目录。之后重新下make。


如果单独编译一个ko文件也可能出现这种情况, 经查看是Module.symvers文件被清空了。 可使用make M=文件夹编译。
