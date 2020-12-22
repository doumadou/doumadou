---
layout: post
title: linux-ftools查看cache缓冲了哪些文件
category: linux
tags: [liunx]
date: 2020-12-22 17:17:46
---

```
# git clone https://github.com/waleedmazhar/linux-ftools
# ./configure
# make
CDPATH="${ZSH_VERSION+.}:" && cd . && /bin/sh /tmp/linux-ftools/missing --run aclocal-1.11 
/tmp/linux-ftools/missing: line 54: aclocal-1.11: command not found
WARNING: `aclocal-1.11' is missing on your system.  You should only need it if
         you modified `acinclude.m4' or `configure.ac'.  You might want
         to install the `Automake' and `Perl' packages.  Grab them from
         any GNU archive site.
 cd . && /bin/sh /tmp/linux-ftools/missing --run automake-1.11 --gnu
/tmp/linux-ftools/missing: line 54: automake-1.11: command not found
WARNING: `automake-1.11' is missing on your system.  You should only need it if
         you modified `Makefile.am', `acinclude.m4' or `configure.ac'.
         You might want to install the `Automake' and `Perl' packages.
         Grab them from any GNU archive site.
CDPATH="${ZSH_VERSION+.}:" && cd . && /bin/sh /tmp/linux-ftools/missing --run autoconf
configure.ac:7: error: possibly undefined macro: AM_INIT_AUTOMAKE
      If this token and others are legitimate, please use m4_pattern_allow.
      See the Autoconf documentation.
make: *** [configure] Error 1
```
这种情况一般是automake与源码中的automake要求的版本不匹配，二种解决方法：安装对应的automake版本；使有系统中的automake，对源码的要求进行修改。

本文使用后一种方法处理：

1. 执行aclocal,产生aclocal.m4文件
```
# aclocal
```

2. 执行autoconf,产生configure文件
```
# autoconf
```

3. 执行automake,产生Makefile.in 
```
# automake
configure.ac:7: warning: AM_INIT_AUTOMAKE: two- and three-arguments forms are deprecated.  For more info, see:
configure.ac:7: http://www.gnu.org/software/automake/manual/automake.html#Modernize-AM_005fINIT_005fAUTOMAKE-invocation
configure.ac:11: error: required file './compile' not found
configure.ac:11:   'automake --add-missing' can install 'compile'
```
若报错，按提示使用 `automake --add-missing`
```
# automake --add-missing
configure.ac:7: warning: AM_INIT_AUTOMAKE: two- and three-arguments forms are deprecated.  For more info, see:
configure.ac:7: http://www.gnu.org/software/automake/manual/automake.html#Modernize-AM_005fINIT_005fAUTOMAKE-invocation
configure.ac:11: installing './compile'

```
4. 再次运行confgure,make即可

编译后产生三个可执行文件:
```
linux-fadvise  linux-fallocate  linux-fincore
```
其中linux-fincore可以用来查看cache中有哪些文件。


用法:

linux-fincore --pages=false --summarize --only-cached * 即可，其中*代表查看当前目录任意文件的cache。也可以指定某个目录/*，表示该目录中的所有文件(但不包括其子目录)。或指定某个具体的文件。


示例:
```
[root@dell-test-dev ~]# /tmp/linux-ftools/linux-fincore  --pages=false --summarize --only-cached /tmp/*
filename                                                                                       size        total_pages    min_cached page       cached_pages        cached_size        cached_perc
--------                                                                                       ----        -----------    ---------------       ------------        -----------        -----------
/tmp/qemu.log                                                                                13,028                  4                  0                  4             16,384             100.00
/tmp/yum_save_tx.2020-12-22.12-14.eOuCRj.yumtx                                                  240                  1                  0                  1              4,096             100.00
---
total cached size: 20,480
# /tmp/linux-ftools/linux-fincore  --pages=false --summarize --only-cached /tmp/linux-ftools/*
filename                                                                                       size        total_pages    min_cached page       cached_pages        cached_size        cached_perc
--------                                                                                       ----        -----------    ---------------       ------------        -----------        -----------
/tmp/linux-ftools/aclocal.m4                                                                 42,141                 11                  0                 11             45,056             100.00
Could not mmap file: /tmp/linux-ftools/autom4te.cache: No such device
/tmp/linux-ftools/config.log                                                                 20,831                  6                  0                  6             24,576             100.00
/tmp/linux-ftools/config.status                                                              29,428                  8                  0                  8             32,768             100.00
/tmp/linux-ftools/configure                                                                 177,892                 44                  0                 44            180,224             100.00
/tmp/linux-ftools/configure.ac                                                                  864                  1                  0                  1              4,096             100.00
Could not mmap file: /tmp/linux-ftools/debian: No such device
/tmp/linux-ftools/depcomp                                                                    17,574                  5                  0                  5             20,480             100.00
/tmp/linux-ftools/INSTALL                                                                     9,416                  3                  0                  3             12,288             100.00
/tmp/linux-ftools/install-sh                                                                 13,184                  4                  0                  4             16,384             100.00
/tmp/linux-ftools/linux-fadvise                                                              22,224                  6                  0                  6             24,576             100.00
/tmp/linux-ftools/linux-fadvise.c                                                             4,875                  2                  0                  2              8,192             100.00
/tmp/linux-ftools/linux-fadvise.o                                                            25,912                  7                  0                  7             28,672             100.00
/tmp/linux-ftools/linux-fallocate                                                            15,712                  4                  0                  4             16,384             100.00
/tmp/linux-ftools/linux-fallocate.c                                                           3,252                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/linux-fallocate.o                                                          17,312                  5                  0                  5             20,480             100.00
/tmp/linux-ftools/linux-fincore                                                              38,984                 10                  0                 10             40,960             100.00
/tmp/linux-ftools/linux-fincore.c                                                            14,967                  4                  0                  4             16,384             100.00
/tmp/linux-ftools/linux-fincore.o                                                            67,184                 17                  0                 17             69,632             100.00
/tmp/linux-ftools/linux-ftools.h                                                                 83                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/Makefile                                                                   24,924                  7                  0                  7             28,672             100.00
/tmp/linux-ftools/Makefile.am                                                                   209                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/Makefile.in                                                                24,641                  7                  0                  7             28,672             100.00
/tmp/linux-ftools/missing                                                                    11,135                  3                  0                  3             12,288             100.00
/tmp/linux-ftools/NEWS                                                                           65                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/README                                                                      6,001                  2                  0                  2              8,192             100.00
/tmp/linux-ftools/RELEASE                                                                       372                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/showrlimit.c                                                                1,961                  1                  0                  1              4,096             100.00
/tmp/linux-ftools/waste_memory.c                                                                699                  1                  0                  1              4,096             100.00
---
total cached size: 667,648
```
