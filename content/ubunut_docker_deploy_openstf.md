---
layout: post
title: ubuntu下使用docker搭建STF
category: linux
tags: [ubuntu, openstf, docker]
date: 2018-10-19 09:41:53
---


1. 下载openstf相关镜像

```
# docker pull openstf/stf:latest  // 拉取stf镜像
# docker pull sorccu/adb:latest  // 拉取adb镜像
# docker pull rethinkdb:latest  // 拉取rethinkdb数据库镜像
# docker pull openstf/ambassador:latest  // 拉取ambassador镜像
# docker pull nginx:latest  // 拉取nginx镜像
```


2. 部署运行容器
```
# docker run -d --name rethinkdb -v /srv/rethinkdb:/data --net host rethinkdb rethinkdb --bind all --cache-size 2048 --http-port 8090 
# docker run -d --name adbd --privileged -v /dev/bus/usb:/dev/bus/usb --net host sorccu/adb:latest 
# docker run -d --name stf --net host openstf/stf stf local
```

然后在浏览器中输入localhost:7100


问题：

1. 设备准备中，不一会就变成断线。
搭建好系统之后 插入手机，打开 http://localhost:7100/#!/devices ，然后查看找到了设备，状态先是prepare 然后过了几秒又 disconnect了。切换了 火狐 google浏览器也是这样的问题。
openstf检测到设备后，会在设备上安装STFService.apk. 如果安装失败，无法与android端的STFService通信，则设备就会变成断开状态。　此时可能是手机上没有打开usb安装程序的权限。
查看日志，有如下报错：
 Setup had an error Error: /data/local/tmp/STFService.apk could not be installed [INSTALL_FAILED_USER_RESTRICTED]
