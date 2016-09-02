---
layout: post
title: Centos7安装nbd模块
category: linux
tags: [linux内核]
date: 2016-08-30 13:08:59
---

# 查看当前内核版本
```
[root@localhost ~]# uname -r
3.10.0-327.28.2.el7.x86_64
```

# 安装kernel开发包
```
# yum install kernel-devel kernel-headers
```

# 下载kernel源码rpm包
根据第一步的kernel内核版本号下载相应的rpm源码包
```
# wget ftp://ftp.icm.edu.pl/vol/rzm5/linux-slc/centos/7.1.1503/updates/Source/SPackages/kernel-3.10.0-327.28.2.el7.src.rpm
```

也可以使用yumdownloader命令进行下载
```
# yumdownloader --source kernel
```

# 安装源码rpm包

```
# rpm -ihv kernel-3.10.0-327.28.3.el7.src.rpm
```
安装完成后在 `~/rpmbuild/SOURCES`路径下会产生一个linux内核源码压缩包。然后解压。

# 解压，编译NDB内核模块

```
# cd  ~/rpmbuild/SOURCES/
# tar vxf linux-3.10.0-327.28.2.el7.tar.xz
# cd linux-3.10.0-327.28.2.el7/
# make mrproper
# cp /usr/src/kernels/$(uname -r)/Module.symvers . -v
# cp /boot/config-$(uname -r) .config . -v
# make oldconfig
# make prepare
# make scripts
# make CONFIG_BLK_DEV_NBD=m M=drivers/block
```

# 安装NDB模块

```
# cp drivers/block/nbd.ko /lib/modules/$(uname -r)/kernel/drivers/block/ -v
# depmod -a
# modprobe nbd max_part=16
# lsmod |grep nbd
```
