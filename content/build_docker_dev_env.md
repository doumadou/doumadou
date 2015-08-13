Title: 搭建docker开发环境
Category: docker
Tags: docker
Date: 2015-08-07 09:34:40
---


##安装依赖

	yum install -y git hg golang sqlite-devel device-mapper-devel btrfs-progs-devel

##下载docker源码

	export GOPATH=/usr/lib/golang
	go get github.com/docker/docker
	

##本地编译

	cd /usr/lib/golang/src/github.com/docker/docker
	
[root@localhost docker]# ./hack/make.sh binary
# WARNING! I don't seem to be running in the Docker container.
# The result of this command might be an incorrect build, and will not be
#   officially supported.
#
# Try this instead: make all
#

bundles/1.5.0 already exists. Removing.

---> Making bundle: binary (in bundles/1.5.0/binary)
daemon/execdriver/native/driver.go:26:2: cannot find package "github.com/docker/libcontainer/console" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/console (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/console (from $GOPATH)
daemon/execdriver/native/create.go:16:2: cannot find package "github.com/docker/libcontainer/mount" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/mount (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/mount (from $GOPATH)
daemon/execdriver/lxc/driver.go:25:2: cannot find package "github.com/docker/libcontainer/mount/nodes" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/mount/nodes (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/mount/nodes (from $GOPATH)
daemon/execdriver/lxc/lxc_init_linux.go:7:2: cannot find package "github.com/docker/libcontainer/namespaces" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/namespaces (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/namespaces (from $GOPATH)
daemon/execdriver/native/driver.go:28:2: cannot find package "github.com/docker/libcontainer/namespaces/nsenter" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/namespaces/nsenter (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/namespaces/nsenter (from $GOPATH)
daemon/execdriver/utils.go:8:2: cannot find package "github.com/docker/libcontainer/security/capabilities" in any of:
	/usr/lib/golang/src/github.com/docker/libcontainer/security/capabilities (from $GOROOT)
	/usr/lib/golang/src/github.com/docker/libcontainer/security/capabilities (from $GOPATH)

提示缺少包，就使用go get 去下载


[root@localhost docker]# go get code.google.com/p/go.net/websocket
//下面是上面的命令执行输出
# cd /usr/lib/golang/src/code.google.com/p/go.net; hg pull
abort: code.google.com certificate error: certificate is for *.googlecode.com, *.cloud.google.com, *.code.google.com, *.codespot.com, *.developers.google.com, *.gcr.io, *.googlesource.com, *.u.googlecode.com, gcr.io, googlecode.com, googlesource.com
(configure hostfingerprint 64:02:da:c9:d5:dc:cb:a8:87:13:4c:a4:6f:ee:e7:dc:fc:c1:8a:42 or use --insecure to connect insecurely)
package code.google.com/p/go.net/websocket: exit status 255
 

若出现以上错误提示，可以手动使用hg去下载代码，　也可以直接修改hg的配置文件（该方法最方便）

方法一: 手动使用hg去下载, 并加上--insecure参数, 例:

~~~ bash
	hg clone --insecure -U https://code.google.com/p/go.net /usr/lib/golang/src/code.google.com/p/go.net
~~~


方法二: 修改hg的配置文件。该方法最好，无需手动下载

注释掉certs.rc中的cacerts项

~~~ bash

[root@localhost docker]# cat /etc/mercurial/hgrc.d/certs.rc
# see: http://mercurial.selenic.com/wiki/CACertificates
#[web]
#cacerts = /etc/pki/tls/certs/ca-bundle.crt

~~~
