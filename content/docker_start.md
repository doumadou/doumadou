Title: 在centos65_x86_64安装体验docker
Date: 2015-07-16 17:00
Category: docker
Tags: docker, paas
Slug: try-docker-in-centos6.5
Author: Gavin
Summary: try docker

##升级kerenl

	# rpm --import https://www.elrepo.org/RPM-GPG-KEY-elrepo.org
	# rpm -Uvh http://www.elrepo.org/elrepo-release-6-6.el6.elrepo.noarch.rpm
	# yum --enablerepo=elrepo-kernel -y install kernel-lt
	修改/etc/grub.conf
	# reboot
	[root@testnode ~]# uname -r
	3.10.82-1.el6.elrepo.x86_64

##安装docker( Docker version 1.5.0, build a8a31ef/1.5.0)

###取消selinux，因为它会干扰lxc的正常功能

	$ sudo vim /etc/selinux/config
	SELINUX=disabled
	SELINUXTYPE=targeted

###安装 Fedora EPEL

	$ sudo yum -y install http://ftp.riken.jp/Linux/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm

###添加 hop5 repo地址

	$ cd /etc/yum.repos.d
	$ sudo wget http://www.hop5.in/yum/el6/hop5.repo

###安装 docker-io

	# sudo yum -y install docker-io

会自动安装带aufs模块的3.10内核，以及docker-io包。

	# yum install -y device-mapper-libs
	# docker images

##制作镜像 centos 6.5

	# yum install -y febootstrap

	mount iso
	
	# mount -o loop /tmp/**.iso /mnt

	# febootstrap centos6.5 centos6.5_image file:///mnt
	##或者将file:///mnt 改为http://vault.centos.org/6.5/os/x86_64/ 从网络安装
	删除不需要的文件夹, 减少镜像大小
	# cd centos6.5_image	
	# cd lib/modules/ && rm 2.6.32-431.el6.x86_64/ -rfv

	# cd -
	
	# cd centos6.5_image && tar -c .|docker import - centos6.5-base

	[root@testnode centos6.5_image]# docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	centos6.5-base      latest              637778da53a4        19 minutes ago      481.2 MB

##启动容器　

	#  docker run -ti centos6.5-base:latest /bin/bash

##获取contianer pid ip
	# docker inspect -f "{{.State.Pid}}" <container name>
	# docker inspect -f "{{.NetworkSettings.IPAddress}}" <container name>

##API:

	# nc -U /var/run/docker.sock
	GET /images/json HTTP/1.1 ## 二个回车
	
	HTTP/1.1 200 OK
	Content-Type: application/json
	Date: Sun, 12 Jul 2015 19:35:33 GMT
	Content-Length: 1009
	
	[{"Created":1436470114,"Id":"d2a0ecffe6fa4ef3de9646a75cc629bbd9da7eead7f767cb810f9808d6b3ecb6","ParentId":"29460ac934423a55802fcad24856827050697b4a9f33550bd93c82762fb6db8f","RepoTags":["ubuntu:14.04","ubuntu:14.04.2","ubuntu:latest","ubuntu:trusty-20150630","ubuntu:trusty"],"Size":0,"VirtualSize":188331689}
	,{"Created":1436391846,"Id":"019c313e5671f01d0deecbb698636d41c7a06af5f5895802939bc63b367a0bb8","ParentId":"5ae2785c4ebfd7fff024e99808012f65b160343f59bfbdd1661791fcfc08ec51","RepoTags":["nginx_1.8.0_php_fpm_5.3.3:v0.1"],"Size":70797331,"VirtualSize":552001511}
	,{"Created":1435787783,"Id":"df74ad94ecc79bdda55062cfbdb0ebcb90bb6c207b4498a3dcc5f92a0b4dd971","ParentId":"2f0fa17ce0b8ac98107cc3bc66436103ee6aec323f9a27f8e67634d602918c58","RepoTags":["mysql_server_5.1.73-5:latest"],"Size":0,"VirtualSize":639244242}
	,{"Created":1435710271,"Id":"637778da53a417bb6c64b029d59382bfc8fb8381943d89377ad312bb9abbbc75","ParentId":"","RepoTags":["centos6.5-base:latest"],"Size":481204071,"VirtualSize":481204071}
	]
	HTTP/1.1 400 Bad Request
	
	[root@testnode go]# docker images
	REPOSITORY                  TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	ubuntu                      trusty-20150630     d2a0ecffe6fa        3 days ago          188.3 MB
	ubuntu                      trusty              d2a0ecffe6fa        3 days ago          188.3 MB
	ubuntu                      14.04               d2a0ecffe6fa        3 days ago          188.3 MB
	ubuntu                      14.04.2             d2a0ecffe6fa        3 days ago          188.3 MB
	ubuntu                      latest              d2a0ecffe6fa        3 days ago          188.3 MB
	nginx_1.8.0_php_fpm_5.3.3   v0.1                019c313e5671        3 days ago          552 MB
	mysql_server_5.1.73-5       latest              df74ad94ecc7        10 days ago         639.2 MB
	centos6.5-base              latest              637778da53a4        11 days ago         481.2 MB

