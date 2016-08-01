---
layout: post
title:  The following packages have unmet dependencies
category: linux
tags: [ubuntu, linux, apt-get]
date: 2016-06-30 09:20:00
---

The following packages have unmet dependencies

# 现象
使用apt-get 安装软件包时出错，出错信息如下：
```
Gavin@ubuntu:/tmp$ sudo apt-get install retext
Reading package lists... Done
Building dependency tree       
Reading state information... Done
You might want to run 'apt-get -f install' to correct these:
The following packages have unmet dependencies:
 google-chrome-stable : Depends: libstdc++6 (>= 4.8.0) but 4.6.3-1ubuntu5 is to be installed
                        Depends: lsb-base (>= 4.1) but 4.0-0ubuntu20 is to be installed
 retext : Depends: python-qt4 but it is not going to be installed
          Depends: python-markdown but it is not going to be installed or
                   python-docutils but it is not going to be installed
          Recommends: retext-wpgen but it is not going to be installed
          Recommends: python-markdown but it is not going to be installed
          Recommends: python-docutils but it is not going to be installed
E: Unmet dependencies. Try 'apt-get -f install' with no packages (or specify a solution).
```

# 原因

上次安装软件(这里是google-chrome-stable, 每个人的情况可能不一样)时，有没有解决的依赖，所以再安装其它软件时会出错。

# 解决方案
要解决这个问题，有２个方案：将上一个软件先安装好；或者就有上次安装出错的软件先删除。这里我们采用先删除上次安装出错的软件，即google-chrome-stable;
删除命令`dpkg --remove google-chrome`
```
Gavin@ubuntu:/tmp$ sudo dpkg --remove google-chrome-stable
(Reading database ... 196810 files and directories currently installed.)
Removing google-chrome-stable ...
Processing triggers for man-db ...
Processing triggers for desktop-file-utils ...
Processing triggers for bamfdaemon ...
Rebuilding /usr/share/applications/bamf.index...
Processing triggers for gnome-menus ...
Processing triggers for menu ...
```
然后继续安装就不会出错了。
```
Gavin@ubuntu:/tmp$  sudo apt-get install retext
Reading package lists... Done
Building dependency tree       
Reading state information... Done
The following packages were automatically installed and are no longer required:
  libjibx1.1-java libtokyocabinet8 libbcel-java libxerces2-java rrdtool libxom-java libdom4j-java simplyhtml libxpp2-java libqdox-java javahelp2
  java-wrappers libjaxen-java freemind-doc libupsclient1 collectd-core libxml-commons-resolver1.1-java libjaxme-java libgnu-regexp-java
  libxml-commons-external-java libjgoodies-forms-java liboping0 libjdom1-java spawn-fcgi libgetopt-java libopenipmi0 libxpp3-java libpq5
  libtokyotyrant3 libcommons-codec-java libbackport-util-concurrent-java liblog4j1.2-java libesmtp6 libmemcached6
Use 'apt-get autoremove' to remove them.
The following extra packages will be installed:
  docutils-common docutils-doc libqt4-designer libqt4-help libqt4-scripttools libqt4-test libqtassistantclient4 libqtwebkit4 python-docutils
  python-markdown python-pygments python-qt4 python-roman python-sip retext-wpgen
Suggested packages:
  texlive-latex-recommended texlive-latex-base texlive-lang-french ttf-linux-libertine python-qt4-dbg python-gdata python-enchant
The following NEW packages will be installed:
  docutils-common docutils-doc libqt4-designer libqt4-help libqt4-scripttools libqt4-test libqtassistantclient4 libqtwebkit4 python-docutils
  python-markdown python-pygments python-qt4 python-roman python-sip retext retext-wpgen
0 upgraded, 16 newly installed, 0 to remove and 291 not upgraded.
Need to get 15.9 MB of archives.
After this operation, 63.9 MB of additional disk space will be used.
Do you want to continue [Y/n]? 
```
