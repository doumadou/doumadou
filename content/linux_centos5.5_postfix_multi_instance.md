Title: Centos5.5系统上安装postfix多实例遇到的问题
Category: linux
Tags: postfix
Date: 2015-10-10 14:12:15
---


Centos5.5系统yum 安装的postfix版本过低, 不支持多实例，因此需要源码编译postfix。

postfix版本: postfix-3.0.2

wget http://mirror.tje.me.uk/pub/mirrors/postfix-release/official/postfix-3.0.2.tar.gz

出现如下警告:
smtpd_sasl_auth_enable is true, but SASL support is not compiled in
处理办法(若不处理,smtp登陆时验证失败。)
# yum install -y cyrus-sasl-devel openssl-devel
# make -f Makefile.init makefiles 'CCARGS=-DUSE_SASL_AUTH -DUSE_CYRUS_SASL -I/usr/include/sasl -DUSE_TLS' 'AUXLIBS=-L/usr/lib/sasl2 -lsasl2 -lssl -lcrypto'
# make && make install

出现如下警告
postfix: warning: smtputf8_enable is true, but EAI support is not compiled in
处理办法（若不处理，发中文邮件将会乱码。所以必须解决）, 解决后支持中文邮件
# for fn in `find /etc/postfix* -name main.cf`;do echo "smtputf8_enable = no" >> $fn;done
# postfix reload


网上流传的方法如下(针对单个实列有用)
# postconf "smtputf8_enable = no"
# postfix reload

如必须支持EAI的话，那么必须源码安装libicu-devel包。(yum 安装的版本太低, 出现如下错误 error: ‘UIDNAInfo’ undeclared)
