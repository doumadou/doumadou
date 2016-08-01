---
layout: post
title: Linux CPU基准测试
category: linux
tags: [linux, 测试]
date: 2016-07-19 16:36:58
---

sysbench是一个模块化的、跨平台、多线程基准性能测试工具，主要用于评估测试各种不同系统参数下的数据库负载情况。关于这个项目的详细介绍请看：https://launchpad.net/sysbench。
它主要包括以下几种方式的测试：
1、cpu性能
2、磁盘io性能
3、调度程序性能
4、内存分配及传输速度
5、POSIX线程性能
6、数据库性能(OLTP基准测试)
目前sysbench主要支持 MySQL,pgsql,oracle 这3种数据库。

# 安装

centos
```
# yum install -y sysbench
```
ubunut
```
# apt-get install -y sysbench
```	

# CPU 测试

```
# sysbench --test=cpu --num-threads=32 --cpu-max-prime=20000 run
sysbench 0.4.12:  multi-threaded system evaluation benchmark

Running the test with following options:
Number of threads: 32

Doing CPU performance benchmark

Threads started!
Done.

Maximum prime number checked in CPU test: 90000


Test execution summary:
    total time:                          105.8817s
    total number of events:              10000
    total time taken by event execution: 3385.1060
    per-request statistics:
         min:                                 30.58ms
         avg:                                338.51ms
         max:                                877.28ms
         approx.  95 percentile:             592.23ms

Threads fairness:
    events (avg/stddev):           312.5000/4.08
    execution time (avg/stddev):   105.7846/0.06

```
cpu测试主要是进行素数的加法运算，在上面的例子中，指定了最大的素数为 20000，自己可以根据机器cpu的性能来适当调整数值。


# 其它测试方法

也可以使用linux 自带的命令bc做测试
```
# time echo "scale=5000;4*a(1)"|bc -l -q
```

time是计时程序。scale是精度，4*a(1）调用了反正切函数。由三角函数我们知道1的反正切是pi/4, pi=4* pi/4。 -l -q参数的意思请参照manpage。这一行其实就是让bc计算1的反正切，计算精度是5000位。
