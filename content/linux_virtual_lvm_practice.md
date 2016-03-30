---
layout: post
title: linux 虚拟lvm实验
category: linux
tags: [lvm, linux]
date: 2016-03-30 09:38:48
---
#linux 虚拟lvm实验

创建2个空的磁盘镜像文件
dd if=/dev/zero of=lvm_pv1.img bs=512K count=40K

挂载为循环设备
losetup /dev/loop0 /work/vdisk/lvm_virtual_pv1.img

#格式化为lvm2格式　
#fdisk /dev/loop0
#n->p-->  t-->8e-->w

创建物理卷
sudo pvcreate /dev/loop1
  Physical volume "/dev/loop1" successfully created

 sudo pvdisplay 
  --- Physical volume ---
  PV Name               /dev/sda5
  VG Name               ubuntu
  PV Size               465.52 GiB / not usable 2.00 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              119173
  Free PE               12
  Allocated PE          119161
  PV UUID               FeGzCf-r8Ix-1iGR-D3VP-zGtL-xasU-NH0OCi
   
  "/dev/loop0" is a new physical volume of "20.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop0
  VG Name               
  PV Size               20.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               sBbkDf-vN96-Kdi6-cis4-M1BW-emx9-e6c8ab
   
  "/dev/loop1" is a new physical volume of "10.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/loop1
  VG Name               
  PV Size               10.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               dEdfLg-OePh-jJp0-UKai-IuPx-e1Lw-ag0VFx


sudo virsh pool-define /etc/libvirt/storage/lvm_pool.xml

 sudo virsh pool-build lvm_pool
 sudo virsh pool-start lvm_pool
