---
layout: post
title: KVM虚拟机磁盘IO性能自动化测试
category: 虚拟化
tags: [kvm]
date: 2016-09-02 11:36:22
---

目标：通过脚本实现对KVM虚拟机自动做快照，模拟用户写入删除文件。自动测快照后的磁盘的IO性能。

对数据盘不停的做外部快照，每完成一次快照后，随机写入部分文件。当达到指定数量的快照后，依次回滚快照，并测试当前快照的IO性能。


虚机里有一个脚本/data2/write_data.sh：实现创建快照后，创建标签文件，并随机写入部分文件，删除部分文件

```
echo "touch /data/TAG_aio_vdb_$1"
touch /data/TAG_aio_vdb_$1

cd /data/

for fn in `find . -name "tekkaman.*" | grep -E '[0-9]|o|j|b' -i`;
do
	rm -rfv $fn;
done


for n in `seq 1 20`;
do
	aa=`mktemp tekkaman.XXX`
	dd if=/dev/urandom of=${aa} bs=1M count=70
done

```

/data为待测磁盘的挂载点。
TAG_aio_vdb_为创建快照后，创建的快照标签文件，用于标签当前为哪个快照。回滚时，测试IO程序，会根据这些文件，测试，并将结果写入特定的文件中。

接下的来for循环为删除文件名中，带数字(0-9), o/O/j/J/b/B的文件。
然后创建20个随机文件名的文件，并写入70M的随机内容。


虚拟机中的开机启动脚本：/data2/init_test.sh

```
#!/bin/bash

cd /data2/

for fn in `find /data -name "TAG_aio*"|sort -r`;
do
	new_iops_name=${fn##/data/TAG_}
	echo $fn
	echo "/usr/local/bin/fio iobench.fio >${new_iops_name}.log && rm -f ${fn} && Shutdown -P now"
	/usr/local/bin/fio iobench.fio >${new_iops_name}.log && rm -f ${fn} && shutdown -P now
	break;
done

```
该脚本功能比较简单：开发后查看最新一个快照名，然后调用fio测试程序，将结果写入快照名对应的文件中。然后删除快照标签文件，并实现关机。


fio配置文件

```
; tiobench like setup, add more fX files between the stonewalls to
; create more threads

[global]
direct=1
ioengine=libaio
size=3072m
bsrange=4k-4k
timeout=60
numjobs=1	; 4 simultaneous threads for each job

[f1]
rw=write
filename=/data/fio_data_test

[f2]
stonewall
rw=randwrite
filename=/data/fio_data_test

[f3]
stonewall
rw=read
filename=/data/fio_data_test

[f4]
stonewall
rw=randread
filename=/data/fio_data_test

```

以上二个文件都必须依赖物理机中的脚本程序。 物理中的脚本在开机状态下，会不停的检测，虚拟中的文件写入进程(/data2/write_data.sh)是否结束，如果结束，则创建快照，并通过virtio通知qga，运行文件写入程序（/data2/write_data.sh). 都创建完指定数量的快照后，再重启虚拟机，并调用另一个脚本程序(checkdomstat.sh)，对虚拟机的状态进行检查，如果虚拟机状态为shut off，则执行回滚快照，启动虚拟机。启动后虚拟机中的开机启动脚本，会完成IO测试，并关机。依次直到所以快照回滚完毕。

```
#/usr/bin/python


import os
import json
import base64
import time

virsh_check_cmd = """virsh qemu-agent-command linux_00_2000000066_2016_08_29_19_12_01 '{"execute": "guest-exec", "arguments":{"path":"/usr/bin/ps", "arg":["-auxf"], "capture-output":true}}'"""
snap_index = 1
while True:
	time.sleep(10)
	pid = None
	with os.popen(virsh_check_cmd, "r") as fp:
		data = fp.read()
		print data
		d = json.loads(data)
		pid = d["return"]["pid"]
		fp.close()
	
	if pid != None:
		virsh_get_cmd_output=""" virsh qemu-agent-command linux_00_2000000066_2016_08_29_19_12_01 '{"execute": "guest-exec-status", "arguments":{"pid":%s}}'""" % pid
		fp = os.popen(virsh_get_cmd_output, "r")
		data = fp.read()
		print data
		try:
			d = json.loads(data)
			base64_str = d["return"]["out-data"]
			exitcode = d["return"]["exitcode"]
			exited = d["return"]["exited"]
		except:
			continue
		ret_body = None
		if exitcode == 0 and exited :
			ret_body = base64.decodestring(base64_str)
	
		if ret_body.find("/data2/write_data.sh") > 0:
			print "conintue check"
			continue

		if snap_index == 10:
			os.system("virsh reboot linux_00_2000000066_2016_08_29_19_12_01")	
			os.system("sh checkdomstat.sh")
			os.exit(1)
	
		print "create snapshot; then run script in guest os"
	
		virsh_snap_create="virsh snapshot-create linux_00_2000000066_2016_08_29_19_12_01 --xmlfile ./snapshot%d_vdb.xml --disk-only" % snap_index
		os.system(virsh_snap_create)
		virsh_run_cmd = """virsh qemu-agent-command linux_00_2000000066_2016_08_29_19_12_01 '{"execute": "guest-exec", "arguments":{"path":"/data2/write_data.sh", "arg":["%d"], "capture-output":true}}'""" % snap_index
		os.system(virsh_run_cmd)
		snap_index = snap_index + 1

```

checkdomstat.sh 文件内容
```
#!/bin/bash

vm_name="linux_00_2000000066_2016_08_29_19_12_01"
#vm_name="test_centos7"
while [ 1 ];
do
	virsh domstate $vm_name |grep "shut off"
	#virsh domstate $vm_name |grep "running"
	if [ $? == "0" ];then
		echo "revert snapshot"
		for sn in `virsh snapshot-list ${vm_name}|grep snapshot|awk '{print $1}'|sort -r`;
		do
			echo "virsh snapshot-delete ${vm_name} ${sn} --metadata"
			virsh snapshot-delete ${vm_name} ${sn} --metadata || exit 1
			sleep 1
			echo "rm -f /var/lib/libvirt/images/test_centos7_data.${sn}"
			rm -f /var/lib/libvirt/images/test_centos7_data.${sn} || exit 1
			sed_flag=0
			for nsn in `virsh snapshot-list ${vm_name}|grep snapshot|awk '{print $1}'|sort -r`;
			do
				echo "sed -i 's/${sn}/${nsn}/g' /etc/libvirt/qemu/${vm_name}.xml"
				sed -i "s/${sn}/${nsn}/g" /etc/libvirt/qemu/${vm_name}.xml || exit 1
				sed -i "s/${sn}/${nsn}/g" /etc/libvirt/qemu/${vm_name}.xml || exit 1
				sed_flag=1
				break
			done
			if [ $sed_flag == 0 ];then
				echo "sed -i 's/${sn}/qcow2/g' /etc/libvirt/qemu/${vm_name}.xml"
				sed -i "s/${sn}/qcow2/g" /etc/libvirt/qemu/${vm_name}.xml || exit 1
				sed -i "s/${sn}/qcow2/g" /etc/libvirt/qemu/${vm_name}.xml || exit 1
			fi
			sleep 2
			echo "virsh define /etc/libvirt/qemu/${vm_name}.xml"
			virsh define /etc/libvirt/qemu/${vm_name}.xml || exit 1
			sleep 1
			echo "virsh start ${vm_name}"
			virsh start ${vm_name} || exit 1

			break;
		done
	else
		echo "next check"
	fi
	sleep 1
done

```
