#!/bin/bash
#########################################################################
# File Name: install_dep.sh
# Author: Gavin Tao
# mail: gavin.tao17@gmail.com
# Created Time: Thu 16 Jul 2015 10:48:13 AM CST
#########################################################################


build_temp='/tmp/build_temp'
url=http://www.crummy.com/software/BeautifulSoup/bs4/download/4.0/beautifulsoup4-4.0.1.tar.gz
[ -d $build_temp ] || mkdir $build_temp
cd $build_temp
pkg_name=`basename $url`
[ -f ${pkg_name} ] || wget $url

tar vxf $pkg_name && cd ${pkg_name%%.tar.gz} && sudo python setup.py install
