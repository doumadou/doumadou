---
layout: post
title: fdisk/gdisk非交互操作操作
category: linux
tags: [liunx]
date: 2017-08-16 16:36:09
---

fdisk/gdisk 非交互操作磁盘

1. 将fdiks/gdisk交互式需要输入的字符命令写入文件。比如叫做gdisk.txt
```
w
y
q
```
文本的内容实际就是我们在交互式时的操作过程需输入的命令。


2. 命令行运行命令
```
# gdisk /tmp/11.img < gdisk.txt
```
