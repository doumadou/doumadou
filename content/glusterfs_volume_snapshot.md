---
layout: post
title: glusterfs 快照功能
category: 分布式文件系统
tags: [glusterfs]
date: 2016-08-04 15:16:11
---

要使用快照功能。glusterfs volume需要满意下列先决条件：

* 每个brick应该在一个独立的thin lvm上。
* brick所在的lv 不能包含其它非brick的数据。
* 不能存在brick存在非thin lvm上。
* gluster版本必须在3.6以上。


使用3台机器组成glusterfs集群。没有多余的lvm。因些使用文件模拟实现。

3台机器IP 分别为 192.168.122.101, 192.168.122.102, 192.168.122.103


192.168.122.101 机器上用文件创建LVM.

```
[root@192-168-233-133 tmp]# dd if=/dev/zero of=bd-loop-thin count=1024 bs=1M
[root@192-168-233-133 5mp]# losetup /dev/loop0 bd-loop-thin
[root@192-168-233-113 tmp]# vgcreate bd-vg /dev/loop0
  Volume group "bd-vg" successfully created
# 创建thin pool
[root@192-168-233-113 tmp]# lvcreate --thin bd-vg -L 1000M
  Logical volume "lvol1" created.
# 创建thin lv
[root@192-168-233-113 tmp]# lvcreate -V 1000M -T /dev/bd-vg/lvol1 -n lv1
  Logical volume "lv1" created.
[root@192-168-233-113 tmp]# lvs
  LV    VG    Attr       LSize    Pool  Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv1   bd-vg Vwi-a-tz-- 1000.00m lvol1        0.00                                   
  lvol1 bd-vg twi-aotz-- 1000.00m              0.00   0.98                            
[root@192-168-233-113 tmp]# mkfs.xfs /dev/bd-vg/lv1 
meta-data=/dev/bd-vg/lv1         isize=256    agcount=8, agsize=31984 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=0        finobt=0
data     =                       bsize=4096   blocks=255872, imaxpct=25
         =                       sunit=16     swidth=16 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
log      =internal log           bsize=4096   blocks=768, version=2
         =                       sectsz=512   sunit=16 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
[root@192-168-233-113 tmp]# mount /dev/bd-vg/lv1 /mnt/
[root@192-168-233-113 tmp]# mkdir /mnt/exp
[root@192-168-233-113 tmp]# lvs
  LV    VG    Attr       LSize    Pool  Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv1   bd-vg Vwi-aotz-- 1000.00m lvol1        0.38                                   
  lvol1 bd-vg twi-aotz-- 1000.00m              0.38   0.98                            
```

192.168.122.102 机器上创建volume, 并建立快照

```
[root@192-168-233-114 ~]# gluster volume create KVMvolume transport tcp 192.168.233.113:/mnt/exp
volume create: KVMvolume: success: please start the volume to access data
[root@192-168-233-114 ~]# gluster volume start KVMvolume
volume start: KVMvolume: success
[root@192-168-233-114 ~]# gluster snapshot create KMVS1 KVMvolume
snapshot create: success: Snap KMVS1_GMT-2016.08.04-07.10.09 created successfully
[root@192-168-233-114 ~]# gluster snapshot list  KVMvolume
KMVS1_GMT-2016.08.04-07.10.09
[root@192-168-233-114 ~]# 
```

建立快照后，192.168.122.101机器上就多了一个lv
```
[root@192-168-233-113 tmp]# lvs
  LV                                 VG    Attr       LSize    Pool  Origin Data%  Meta%  Move Log Cpy%Sync Convert
  8e613eda9f0749618abe6aad65eef1b2_0 bd-vg Vwi-aotz-- 1000.00m lvol1 lv1    0.42                                   
  lv1                                bd-vg Vwi-aotz-- 1000.00m lvol1        0.42                                   
  lvol1                              bd-vg twi-aotz-- 1000.00m              0.67   1.07  
```
