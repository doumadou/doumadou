---
layout: post
title: 使用nexe将nodejs编译成一个独立可执行文件
category: nodejs
tags: [nodejs, nexe]
date: 2017-01-16 15:09:36
---

使用nexe编译nodejs文件，有二种方法；

第一种: 安装nexe

安装nexe
```
yum install npm
npm install nexe
```

编译文件
```
./node_modules/nexe/bin/nexe  -i input.js -o input # 第一次执行时，该命令会下载最新版的nodejs,并编译，因此时间会比较久。
```

第二种：使用docker-nexe镜像编译


前提：需要安装docker

下载docker镜像
```
# sudo docker pull asbjornenge/nexe-docker
```

运行docker编译 nodejs (--rm 参数表示，使用编译完成后，删除该窗器)
```
# docker run -v $(pwd):/app --rm -w /app asbjornenge/nexe-docker -i input.js -o app.bin
```
