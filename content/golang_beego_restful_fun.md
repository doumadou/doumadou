Title: 使用Beego搭建RESTFUL服务
Category:  golang
Tags: beego, golang
Date: 2015-08-10 23:59:41
---

##安装Beego

	go get github.com/astaxie/beego
	go get github.com/astaxie/bee
	bee是beego的一个工具，能够快速的创建项目


##创建API项目

	bee api RrojectName

##测试

	启动服务
	cd ProjectName
	go run main.go

	curl  http://107.150.46.106:8080/v1/user/
	或
	wget http://107.150.46.106:8080/v1/user/

##使用API自动化文档

	cd ProjectName
	wget https://github.com/beego/swagger/archive/v1.tar.gz
	tar vxf v1.tar.gz
	mv swagger-1/ swagger
	

启动服务后，浏览器输入http://127.0.0.1:8080/swagger/#!/object
