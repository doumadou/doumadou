---
layout: post
title: libvirt通过qmp协议与qemu-monitor通信
category: kvm
tags: [libvirt, qemu, qemu-monitor, qmp]
date: 2016-04-08 14:10:22
---

# 获取balloon信息, hmp格式
~~~
	#virsh qemu-monitor-command domain_name --hmp  'info balloon'
	balloon: actual=1024
~~~

# 获取guest-stats

~~~
	# virsh qemu-monitor-command domain_name '{"execute":"qom-get", "arguments" : { "path" : "//machine/i440fx/pci.0/child[11]" , "property" : "guest-stats" }}'
{"return":{"stats":{"stat-swap-out":0,"stat-free-memory":802586624,"stat-minor-faults":1985905,"stat-major-faults":445,"stat-total-memory":1041391616,"stat-swap-in":0},"last-update":1460096372},"id":"libvirt-485"}
~~~

上面的命令可获取guest的实际内存，空闭内存，swap信息。前提是虚拟机中需要安装virtio-balloon模块,虚拟机配置文件中需要添加balloon设备，否则只能获取stat-total-memory. 
```
    <memballoon model='virtio'>
      <stats period='10'/>
    </memballoon>
```

命令中的path，是指虚拟机 balloon设备的path. 我是通过libvirt的日志调试输出，获取的path。后面我也试着通过一级一级的查询pci-ballon设备，获取path. 如果有好的其它的方法，请留言告之，谢谢。

```
# virsh qemu-monitor-command domain_name '{"execute":"qom-list","arguments":{"path":"/"}}'
{"return":[{"name":"machine","type":"child<pc-i440fx-2.4-machine>"},{"name":"type","type":"string"},{"name":"objects","type":"child<container>"},{"name":"backend","type":"child<container>"}],"id":"libvirt-490"}

# virsh qemu-monitor-command domain_name '{"execute":"qom-list","arguments":{"path":"/machine"}}'
{"return":[{"name":"dump-guest-core","type":"bool"},{"name":"type","type":"string"},{"name":"append","type":"string"},{"name":"initrd","type":"string"},{"name":"enforce-aligned-dimm","type":"bool"},{"name":"peripheral-anon","type":"child<container>"},{"name":"i440fx","type":"child<i440FX-pcihost>"},{"name":"max-ram-below-4g","type":"size"},{"name":"kernel","type":"string"},{"name":"acpi-device","type":"link<hotplug-handler>"},{"name":"kernel-irqchip","type":"bool"},{"name":"iommu","type":"bool"},{"name":"unattached","type":"child<container>"},{"name":"dt-compatible","type":"string"},{"name":"firmware","type":"string"},{"name":"smm","type":"OnOffAuto"},{"name":"accel","type":"string"},{"name":"suppress-vmdesc","type":"bool"},{"name":"kvm-shadow-mem","type":"int"},{"name":"phandle-start","type":"int"},{"name":"smram","type":"link<qemu:memory-region>"},{"name":"dtb","type":"string"},{"name":"dumpdtb","type":"string"},{"name":"igd-passthru","type":"bool"},{"name":"usb","type":"bool"},{"name":"rtc_state","type":"link<isa-device>"},{"name":"vmport","type":"OnOffAuto"},{"name":"mem-merge","type":"bool"},{"name":"peripheral","type":"child<container>"},{"name":"fw_cfg","type":"child<fw_cfg_io>"},{"name":"hotplug-memory-region-size","type":"int"},{"name":"rtc-time","type":"struct tm"}],"id":"libvirt-491"}

# virsh qemu-monitor-command domain_name '{"execute":"qom-list","arguments":{"path":"/machine/i440fx/"}}'
{"return":[{"name":"pam-pci[4]","type":"child<qemu:memory-region>"},{"name":"pam-pci[15]","type":"child<qemu:memory-region>"},{"name":"pam-pci[0]","type":"child<qemu:memory-region>"},{"name":"pci.0","type":"child<PCI>"},{"name":"pam-pci[11]","type":"child<qemu:memory-region>"},{"name":"type","type":"string"},{"name":"pam-ram[6]","type":"child<qemu:memory-region>"},{"name":"parent_bus","type":"link<bus>"},{"name":"pam-rom[8]","type":"child<qemu:memory-region>"},{"name":"pam-ram[2]","type":"child<qemu:memory-region>"},{"name":"hotplugged","type":"bool"},{"name":"pam-rom[4]","type":"child<qemu:memory-region>"},{"name":"pam-ram[12]","type":"child<qemu:memory-region>"},{"name":"pam-pci[7]","type":"child<qemu:memory-region>"},{"name":"pam-pci[22]","type":"child<qemu:memory-region>"},{"name":"pam-rom[0]","type":"child<qemu:memory-region>"},{"name":"pam-pci[18]","type":"child<qemu:memory-region>"},{"name":"pam-pci[3]","type":"child<qemu:memory-region>"},{"name":"pci-hole-end","type":"int"},{"name":"pam-pci[14]","type":"child<qemu:memory-region>"},{"name":"pam-pci[10]","type":"child<qemu:memory-region>"},{"name":"pci-hole64-start","type":"int"},{"name":"pam-ram[9]","type":"child<qemu:memory-region>"},{"name":"pci-conf-data[0]","type":"child<qemu:memory-region>"},{"name":"pam-ram[5]","type":"child<qemu:memory-region>"},{"name":"pam-rom[7]","type":"child<qemu:memory-region>"},{"name":"pam-rom[12]","type":"child<qemu:memory-region>"},{"name":"hotpluggable","type":"bool"},{"name":"pci-hole64-size","type":"size"},{"name":"pam-ram[1]","type":"child<qemu:memory-region>"},{"name":"ioapic","type":"child<kvm-ioapic>"},{"name":"pam-pci[25]","type":"child<qemu:memory-region>"},{"name":"pam-rom[3]","type":"child<qemu:memory-region>"},{"name":"pam-pci[6]","type":"child<qemu:memory-region>"},{"name":"pam-pci[21]","type":"child<qemu:memory-region>"},{"name":"pam-ram[11]","type":"child<qemu:memory-region>"},{"name":"pam-pci[17]","type":"child<qemu:memory-region>"},{"name":"short_root_bus","type":"uint32"},{"name":"pam-pci[2]","type":"child<qemu:memory-region>"},{"name":"realized","type":"bool"},{"name":"pam-pci[13]","type":"child<qemu:memory-region>"},{"name":"pam-ram[8]","type":"child<qemu:memory-region>"},{"name":"pam-ram[4]","type":"child<qemu:memory-region>"},{"name":"pam-ram[0]","type":"child<qemu:memory-region>"},{"name":"pam-rom[6]","type":"child<qemu:memory-region>"},{"name":"pam-rom[11]","type":"child<qemu:memory-region>"},{"name":"pam-pci[9]","type":"child<qemu:memory-region>"},{"name":"pam-pci[24]","type":"child<qemu:memory-region>"},{"name":"pam-rom[2]","type":"child<qemu:memory-region>"},{"name":"pam-pci[5]","type":"child<qemu:memory-region>"},{"name":"pam-pci[20]","type":"child<qemu:memory-region>"},{"name":"pam-ram[10]","type":"child<qemu:memory-region>"},{"name":"pam-pci[16]","type":"child<qemu:memory-region>"},{"name":"pci-hole64-end","type":"int"},{"name":"pam-pci[1]","type":"child<qemu:memory-region>"},{"name":"pam-pci[12]","type":"child<qemu:memory-region>"},{"name":"pam-ram[7]","type":"child<qemu:memory-region>"},{"name":"pci-conf-idx[0]","type":"child<qemu:memory-region>"},{"name":"pam-rom[9]","type":"child<qemu:memory-region>"},{"name":"pam-ram[3]","type":"child<qemu:memory-region>"},{"name":"pci-hole-start","type":"int"},{"name":"pam-rom[5]","type":"child<qemu:memory-region>"},{"name":"pam-rom[10]","type":"child<qemu:memory-region>"},{"name":"pam-pci[8]","type":"child<qemu:memory-region>"},{"name":"pam-pci[23]","type":"child<qemu:memory-region>"},{"name":"pam-rom[1]","type":"child<qemu:memory-region>"},{"name":"pam-pci[19]","type":"child<qemu:memory-region>"}],"id":"libvirt-492"}

# virsh qemu-monitor-command domain_name '{"execute":"qom-list","arguments":{"path":"/machine/i440fx/pci.0"}}'
{"return":[{"name":"child[6]","type":"link<virtio-blk-pci>"},{"name":"child[5]","type":"link<virtio-serial-pci>"},{"name":"child[4]","type":"link<piix3-usb-uhci>"},{"name":"child[3]","type":"link<PIIX4_PM>"},{"name":"hotplug-handler","type":"link<hotplug-handler>"},{"name":"child[2]","type":"link<piix3-ide>"},{"name":"child[1]","type":"link<PIIX3>"},{"name":"child[0]","type":"link<i440FX>"},{"name":"child[11]","type":"link<virtio-balloon-pci>"},{"name":"type","type":"string"},{"name":"child[9]","type":"link<cirrus-vga>"},{"name":"acpi-pcihp-bsel","type":"uint32"},{"name":"child[8]","type":"link<rtl8139>"},{"name":"child[7]","type":"link<rtl8139>"},{"name":"realized","type":"bool"},{"name":"child[10]","type":"link<intel-hda>"}],"id":"libvirt-493"}
```


