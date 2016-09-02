---
layout: post
title: centos7 通过yum 安装jewel版本ceph
category: ceph
tags: [ceph, jewel]
date: 2016-08-26 09:36:13
---

# 删除默认的源，国外的比较慢

```
yum clean all
rm -rf /etc/yum.repos.d/*.repo
```

# 下载阿里云的base源

```
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
```

下载阿里云的epel源

```
wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
```

修改里面的系统版本为7.2.1511,当前用的centos的版本的的yum源可能已经清空了

```
sed -i '/aliyuncs/d' /etc/yum.repos.d/CentOS-Base.repo
sed -i '/aliyuncs/d' /etc/yum.repos.d/epel.repo
sed -i 's/$releasever/7.2.1511/g' /etc/yum.repos.d/CentOS-Base.repo
```

添加ceph源

```
vim /etc/yum.repos.d/ceph.repo
```

添加
```
[ceph]
name=ceph
baseurl=http://mirrors.aliyun.com/ceph/rpm-jewel/el7/x86_64/
gpgcheck=0
[ceph-noarch]
name=cephnoarch
baseurl=http://mirrors.aliyun.com/ceph/rpm-jewel/el7/noarch/
gpgcheck=0
[ceph-source]
name=cephsource
baseurl=http://mirrors.aliyun.com/ceph/rpm-jewel/el7/SRPMS/
gpgcheck=0
priority=1
```
注意：网上有很多版本都没有[ceph-source]这个结点。但这个结点很重要，没有话，安装ceph, ceph-depoly不会有问题，但用deploy安装集群时会出错，所以记得一定要添加。


进行yum的makecache

```
yum makecache
```

安装软件

```
yum install -y ceph ceph-deploy
```

