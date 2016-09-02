---
layout: post
title: centos7上部署ceph集群
category: ceph
tags: [ceph]
date: 2016-08-26 10:02:51
---

# 设置ceph源
# 安装ceph-deploy, ceph

# ssh 相互免密码
# ssh 相互首次登陆去输入yes
# 同步下时间(所有机器)
搞分布式跟机器对时间都是有要求的。
# 设置hosts绑定，修改hostname
例：
```
192.168.230.101 osd1
192.168.230.101 mon1
192.168.230.123 osd2
192.168.230.124 osd3
```

# 初始化集群
集群的部署，使用ceph-deploy.ceph-deploy的工作原理跟fabric类似： 通过ssh登录到机器上执行一些安装部署命令

```
# ceph-deploy new mon1
```
初始化成功后，会在当前目录下生成ceph.conf文件。修改该文件。

```
[global]
fsid = 230de6f6-71a8-442c-b656-158c4a36920d
mon_initial_members = mon1
mon_host = 192.168.230.101
auth_cluster_required = cephx
auth_service_required = cephx
auth_client_required = cephx

### 以下是添加的部分###

filestore_xattr_use_omap = true
mds_max_file_size = 10240000
mds_cache_size = 102400
osd_journal_size = 1024
osd_pool_default_size = 2       #pool size这些参数需要注意点
osd_pool_default_min_size = 1
osd_crush_chooseleaf_type = 1
osd_recovery_threads = 1
osd_mkfs_type = xfs
rbd_default_features = 3   #这个参数很关键 新版得配置这个参数不然块存储那块 map不上

```

# 在所有结点上安装ceph

```
# ceph-deploy install osd1 osd2 osd3
```

当前集群只有三个结点，分别osd1, osd2, osd3 (osd1与mon1是同一个结点). 


# 初始化mon节点 

```
# ceph-deploy mon create-initial
```

初始化成功后，会在mon1结点上启动ceph-mon进程。

# 初始化osd磁盘

```
# ceph-deploy disk zap osd1:vdc
# ceph-deploy osd create osd1:/dev/vdc

# ceph-deploy disk zap osd2:vdc
# ceph-deploy osd create osd2:/dev/vdc

# ceph-deploy disk zap osd3:vdc
# ceph-deploy osd create osd3:/dev/vdc
```

部署完成后osd节点上会把osd磁盘挂载到 /var/lib/ceph/osd/ceph-{osd-id}目录下

# 检测ceph集群状态

```
# ceph health   #然后OK就代表整个部署是ok的

HEALTH_OK
```


# 测试块存储

首先创建一个pool 专门做块存储的

```
# ceph osd pool create cinder 30
# ceph osd pool set cinder size 2
# ceph osd lspools  #查看pool是否新建ok
0 rbd,1 cinder,
或
# rados lspools
rbd
cinder

```
如无rbd命令，则需要安装rdb命令(ceph-common)

创建镜像: 在cinder pool下创建一个大小为1024M 名称为one的镜像

```
# rbd create -p cinder -s 1024M one
# rbd ls -p cinder -l
NAME  SIZE PARENT FMT PROT LOCK 
one  1024M          2     
```


```
[root@192-168-230-124 ~]# rbd map -p cinder one
/dev/rbd0
[root@192-168-230-124 ~]# fdisk /dev/rbd0
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0xfa390d41.

Command (m for help): p

Disk /dev/rbd0: 1073 MB, 1073741824 bytes, 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 4194304 bytes / 4194304 bytes
Disk label type: dos
Disk identifier: 0xfa390d41

     Device Boot      Start         End      Blocks   Id  System

Command (m for help): q

[root@192-168-230-124 ~]# mkfs.ext4 /dev/rbd0 
mke2fs 1.42.9 (28-Dec-2013)
Discarding device blocks: done                            
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=1024 blocks, Stripe width=1024 blocks
65536 inodes, 262144 blocks
13107 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=268435456
8 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
	32768, 98304, 163840, 229376

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done

[root@192-168-230-124 ~]# mount /dev/rbd0 /mnt/
[root@192-168-230-124 ~]# cd /mnt/
[root@192-168-230-124 mnt]# dd if=/dev/zero of=test.img bs=512K count=1000
1000+0 records in
1000+0 records out
524288000 bytes (524 MB) copied, 4.73188 s, 111 MB/s
[root@192-168-230-124 mnt]# df -m
Filesystem     1M-blocks  Used Available Use% Mounted on
/dev/vda1          61425  1950     59475   4% /
devtmpfs             488     0       488   0% /dev
tmpfs                497     0       497   0% /dev/shm
tmpfs                497     7       490   2% /run
tmpfs                497     0       497   0% /sys/fs/cgroup
tmpfs                100     0       100   0% /run/user/0
/dev/vdc1           9205   846      8360  10% /var/lib/ceph/osd/ceph-2
/dev/rbd0            976   503       407  56% /mnt
```

