---
layout: post
title: Linux挂载新增磁盘
category: linux
tags: [linux]
date: 2016-07-22 13:37:48
---

对于用户新增加的数据盘。用户可以直接当裸设备直接使用。否则需要经过分区，格式化，挂载等步骤才能够使用新增加的数据盘。新增加的数据盘为vdc。

# 查看硬盘分布和对新硬盘进行分区

使用`fdisk -l`命令查看目前系统上已有几块硬盘及分区。

```
[root@biggeryun ~]# fdisk -l

Disk /dev/vda: 64.4 GB, 64424509440 bytes, 125829120 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x000aee74

   Device Boot      Start         End      Blocks   Id  System
/dev/vda1   *        2048   125827071    62912512   83  Linux

Disk /dev/vdb: 2147 MB, 2147483648 bytes, 4194304 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/vdc: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

[root@biggeryun ~]# 
```
根据命令输出的结果，可以看到/dev/vdc，容量10.7G，切未被分区. 这就是新增的一块磁盘。非裸盘使用者，需要对其进行分区，建立相对应的文件系统后才能存储文件。

# 磁盘分区
使用fdisk对/dev/vdc磁盘进行分区. 命令`fdisk /dev/vdc`

## 查看分区信息
输入`fdisk /dev/vdc`回车，进入fdisk交互操作模块，然后输入`p`并回车, 输出分区信息。
```
[root@biggeryun ~]# fdisk /dev/vdc
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x1cc585c4.

Command (m for help): p

Disk /dev/vdc: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x1cc585c4

   Device Boot      Start         End      Blocks   Id  System

Command (m for help):
```

## 创建分区

继上，继续输入`n`并回车, 然后一直回车，直接再次出现"Command (m for help): ".  出现"Command (m for help):"说明需要输入fdisk相应的操作命令才能继续。输入`p`并回车，即可显示刚才创建的分区`/dev/vdc1`。创建成功后，输入`w`并回车，保存分区信息，并退出。
```
[root@biggeryun ~]# fdisk /dev/vdc
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x43b587ba.

Command (m for help): p

Disk /dev/vdc: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x43b587ba

   Device Boot      Start         End      Blocks   Id  System

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): 
Using default response p
Partition number (1-4, default 1): 
First sector (2048-20971519, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): 
Using default value 20971519
Partition 1 of type Linux and of size 10 GiB is set

Command (m for help): p

Disk /dev/vdc: 10.7 GB, 10737418240 bytes, 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk label type: dos
Disk identifier: 0x43b587ba

   Device Boot      Start         End      Blocks   Id  System
/dev/vdc1            2048    20971519    10484736   83  Linux

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.

```

# 创建文件系统
磁盘分区只有在创建文件系统后才能使用，这一过程称为格式化。 根据自己的需求的文件系统的类型，创建特定的文件系统。本例中使用xfs文件系统。如果对文件系统不熟悉，建议centos7使用xfs文件系统，centos6.8, ubuntu14.04 ubuntu16.04 使用ext4文件系统。
使用的命令格式为`mkfs.` + 文件系统名称，例：格式化xfs文件系统的命令为`mkfs.xfs`
```
[root@biggeryun ~]# mkfs.xfs /dev/vdc1 
meta-data=/dev/vdc1              isize=256    agcount=4, agsize=655296 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=0        finobt=0
data     =                       bsize=4096   blocks=2621184, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=0
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
```
注意：　不同的文件系统，输出结果不一样。

# 挂载文件系统
修改/etc/fstab，使系统启动就可以自动挂载，也可以用mount命令挂载。

* 创建挂载点
即创建一个文件夹。挂载点的名称，可以任意（尽量不要使用已存在的文件夹名称作为挂载点）。
```
[root@biggeryun ~]# mkdir /biggeryun
[root@biggeryun ~]# 
```

* 修改fstab
修改fstab前，先备份一下fstab文件(用于文件改错时修复).
```
[root@biggeryun ~]# cp /etc/fstab /etc/fstab.bak
[root@biggeryun ~]# 
```
向fstab文件中添加一条文件系统相关信息
```
[root@biggeryun ~]# echo "/dev/vdc1          /biggeryun       xfs      defaults    0 0" >> /etc/fstab
[root@biggeryun ~]# 
```
说明: "/dev/vdc1"为刚才新增的分区，　"/biggeryun" 为刚才创建的挂载点, "xfs"为格式化/dev/vdc1分区的文件系统类型。需要根据自己的情况，修改这三个内容。


* 挂载
如果没有重启，需要使用mount命令手动挂载。当重启后，就会自动挂载，无需再手动挂载。
```
[root@biggeryun ~]# mount /biggeryun/
[root@biggeryun ~]# df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/vda1       62897156 1746332  61150824   3% /
devtmpfs          499020       0    499020   0% /dev
tmpfs             508376       0    508376   0% /dev/shm
tmpfs             508376    6680    501696   2% /run
tmpfs             508376       0    508376   0% /sys/fs/cgroup
tmpfs             101676       0    101676   0% /run/user/0
/dev/vdc1       10474496   32928  10441568   1% /biggeryun
[root@biggeryun ~]# 
```
说明: 运行mount命令后，通过df命令，可以看/dev/vdc1，已经成功挂载到/biggeryun。

挂载成功后，文件存放到/biggeryun文件夹中，就相当于存储到新增的磁盘上。

