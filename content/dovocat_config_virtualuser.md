Title: dovecot配置虚拟用户
Category: linux
Tags: dovecot, pop3
Date: 2015-08-12 17:11:08
---


##添加一个用户

	useradd vuser
	echo "vuser" |passwd --stdin vuser
	
查看uid, gid

	cat /etc/passwd | grep ^vuser -w|awk -F: '{print $3}'
	500


##修改mail_uid, mail_gid, mail_location

假设上面查到的uid, gid为500, 修改/etc/dovecot/conf.d/10-mail.conf

	mail_uid = 500
	mail_gid = 500
	mail_location = mbox:/home/vuser/var/mail/%u

##修改password配置文件

修改/etc/dovecot/conf.d/auth-passwdfile.conf.ext

内容如下:

	userdb passwd-file {
	  driver = passwd-file
	  args = /etc/dovecot/users
	}
	passdb passwd-file {
	  driver = passwd-file
	  args = /etc/dovecot/users
	}


##添加虚拟用户

直接找开/etc/dovecot/users文件添加即可

passdb文件格式

	user:password

使用doveadm加密密码。 我用的是PLAIN加密方式, 添加一个test的虚拟用户，密码为123456

	doveadm pw -u test -p 123456 -s PLAIN
	{PLAIN}123456	

在/etc/dovecot/users中添加用户

	test:{PLAIN}123456

##常见问题

1. Error: user test: Couldn't drop privileges: Mail access not allowed for root
出现这个错误说明不允许root访问， 所以需要修改mail_uid, mail_gid
