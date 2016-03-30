---
layout: post
title: vim 命令实现文件奇数行与偶数行互换
category: vim
tags: [vim]
date: 2016-03-30 09:31:30
---

<pre>
:%s/\(^.*$\)\n\(^.*$\)/\2\r\1/g
</pre>
