---
layout: post
title: php去掉宽字符空白符
category: php
tags: [php, unicode]
date: 2016-07-12 11:58:11
---


```
preg_replace('/^[\pZ\pC]+|[\pZ\pC]+$/u','',$str);
```
