---
layout: post
title: Libvirt透传qemu命令行参数
category: 虚拟化
tags: [libvirt, qemu]
date: 2016-09-06 16:16:56
---


修改xml
为
```
<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
```


在xml顶层结点下添加
```<qemu:commandline>``` 标签

例添加ROM选项:

```
<qemu:commandline>
   <qemu:arg value='-option-rom'/>
   <qemu:arg value='path/to/my.rom'/>
</qemu:commandline>
```

例：给qcow2文件添加l2-cache-size和refcount-cache-size

```
<qemu:commandline>
   <qemu:arg value='-drive'/>
   <qemu:arg value='file=/var/lib/libvirt/images/test.qcow2,cache-size=10485760,if=none,id=drive-virtio-disk2,format=qcow2,cache=writeback,aio=threads'/>
   <qemu:arg value='-device'/>
   <qemu:arg value='virtio-blk-pci,scsi=off,bus=pci.0,addr=0x9,drive=drive-virtio-disk2,id=virtio-disk2'/>
</qemu:commandline>

```
