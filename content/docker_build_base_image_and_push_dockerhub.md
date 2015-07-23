Title: docker制作centos6.5基础镜像并上传docker hub
Date: 2015-07-21 17:09
Category: docker
Tags: docker
Slug: build-docker-base-image-push-hub
Author: Gavin
Summary: docker制作基础镜像


##制作基础镜像

	# yum install -y febootstrap
	# febootstrap centos6.5 centos6.5_image http://vault.centos.org/6.5/os/x86_64/
	# 删除不需要的文件夹，减少镜像大小, 由于docker容器与宿主机共享内核，所以可以将内核模块删除。注意，别由于输入错误，而将宿主机的模块删除了。
	# cd centos6.5_image	
	# cd lib/modules/ && rm 2.6.32-431.el6.x86_64/ -rfv
	# cd -
    # 打包，导入镜像
	# cd centos6.5_image && tar -c .|docker import - centos6.5-base

	[root@testnode centos6.5_image]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
centos6.5-base      latest              637778da53a4        19 minutes ago      481.2 MB
 
可以基础镜像已经制作成功了。

##将制作好的镜像上传到docker hub.

###注册docker hub账号
已经注册可以忽略, 注册链接：
<a href="https://hub.docker.com/account/signup/">注册</a>

###登陆docker账号
已经登陆可以忽略

	# docker login
    # 根据提示输入账号信息即可

###Push镜像到docker hub

docker hub上存储镜像的格式为 <username>/<imagename>[:TAG], 所以先在本地将image的格式规范下。　使用docker tag 命令

	# docker tag centos6.5-base <username>/<imagename>
	# docker push <username>/<imagename>
	637778da53a4: Image successfully pushed 
	Pushing tag for rev [637778da53a4] on {https://cdn-registry-1.docker.io/v1/repositories/<username>/<imagename>/tags/latest}

近500Ｍ的镜像一下子就上传完成了。感觉很爽啊^-^。
