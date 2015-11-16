Title: Linux systemtap安装测试
Categories: 内核
Tags: systemtap, kernel
Date: 2015-11-11 13:58:01
---


环境:

操作系统: ubuntu 12.04

内核版本:(uname -r) 3.14.12

systemtap版本: git://sourceware.org/git/systemtap.git (HEAD:b3fbdd3ef628d9ec2f64fa6cdb2cb61f9da5a8d8)

系统自动的版本(systemtap - instrumentation system for Linux 2.6)是针对Linux 2.6的内核，所以需要源码安装systemtap. 


1. 安装systemtap

~~~
	$ sudo apt-get install gettext libdw-dev
~~~

2. 编译systemtap

~~~
	$ ./configure --prefix=/user
	$ make
	$ sudo make install
~~~

3. 测试


~~~
	$ sudo stap -e 'probe begin { log("hello world") exit() }'
~~~
如果没有出错，说明安装成功。
