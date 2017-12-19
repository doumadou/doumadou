---
layout: post
title: x509 certificate signed by unknown authority
category: linux
tags: [linux, golang]
date: 2017-12-19 16:27:14
---

golang GET https出错
```
x509 certificate signed by unknown authority
```

可以通过修改client代码解码。
也可以通过如下方式解决.

安装
```
yum install -y ca-certificates
```

