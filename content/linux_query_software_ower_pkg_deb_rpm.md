Title: 查看命令所属的deb/rpm包
Category: linux
Tags: deb, rpm
Date: 2015-10-08 12:34:12
---


deb系列

~~~bash
	$ dpkg -S `which ip`
~~~

rpm系列

~~~ bash
	$ rpm -qf `which ip`
~~~
