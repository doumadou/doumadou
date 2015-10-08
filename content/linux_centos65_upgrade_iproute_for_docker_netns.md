Title: Centos 6.5升级iproute
Category: linux
Tags: iproute, netns
Date: 2015-10-08 14:30:29
---


Centos 6.5升级iproute


##ip netns “Object "netns" is unknown, try "ip help".\n'”报错错误 请安装如下包:

###
	# wget https://repos.fedorapeople.org/openstack/EOL/openstack-grizzly/epel-6/iproute-2.6.32-130.el6ost.netns.2.x86_64.rpm
    # rpm -ivhU ./iproute-2.6.32-130.el6ost.netns.2.x86_64.rpm 
###



