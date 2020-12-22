---
layout: post
title: fio做数据一致性验证测试
category: linux
tags: [fio]
date: 2020-10-22 11:57:17
---


写入测试命令
```
# fio -direct=1 -rw=write -verify=md5 -verify_pattern=0x12345678 -do_verify=1 -verify_dump=1 -bs=4k -size=1G -numjobs=1 -ioengine=libaio -iodepth=128 -name=file1 -output=file1.iops -filename=/tmp/img
```
verify表示校验使用md5哈希算法
verify_pattern表示数据生成模式全用0x12345678填空。
verify_dump表示的是如果校验识别,把失败的数据dump到本地文件中,下面是一个示例:

写数据填空格式
包含一个verify_header,内容如下:
```
struct verify_header {
	uint16_t magic;
	uint16_t verify_type;
	uint32_t len;
	uint64_t rand_seed;
	uint64_t offset;
	uint32_t time_sec;
	uint32_t time_usec;
	uint16_t thread;
	uint16_t numberio;
	uint32_t crc32;
};
```
参考: https://github.com/axboe/fio/blob/4fff54ccba73aa59de250a0f4161b9ce3d952601/verify.h
大小刚好是48bytes.接下来是8字节校验值，例如md5的话，那就是md5检验码，后面就是填充数据. 

正常验证没任何特别的提示。弄一个错误的例子做验证。


第一步, 启动fio测试命令
```
# fio -direct=1  -rw=write --verify=md5 -verify_pattern=0x12345678 -do_verify=1 -verify_dump=1 -bs=4k -size=1G -numjobs=1 -ioengine=libaio -iodepth=128 -name=file1 -output=file1.iops -filename=/tmp/img
```
为了更好的模拟出错，最好使用顺序写，因为如果使用随机写的话，修改错误的时机不好把握，可能会出现verify报错不准确，或不报的情况。

第二步，等到fio命令快结束时，修改文件内容，模拟写入出错的场景. 这里修改1M位位置前后的二个字节。等到fio写了1M字节后就可以执行该命令了。
```
# echo "fffff:eeee" |xxd -r - /tmp/img
```

最后fio命令执行完成后，会在终端输出错误信息
```
md5: verify failed at file /tmp/img offset 1044480, length 4096OPS][eta 01m:54s]
       Expected CRC: 0819950a73ff030bc173be56a8ba274e
       Received CRC: 271e6b3aeee3985d7340112d8eae74d5
       received data dumped as img.1044480.received
       expected data dumped as img.1044480.expected
verify: bad magic header acee, wanted acca at file /tmp/img offset 1048576, length 4096
       hdr_fail data dumped as img.1048576.hdr_fail
```
0xfffff为1048575，以4k为块，该地址正好位于前一个块的结构，会修改前一个块的结尾的一个字节，跟后一个块的开买的字节，因此有二个块的校验会出错. 前一个块是最后一个字节出错。后一个块的开头出错，因此报校验magic出错。

原始数据
```
[root@localhost tmp]# xxd -s 0xffff0 /tmp/img  |head
00ffff0: 1234 5678 1234 5678 1234 5678 1234 56ee  .4Vx.4Vx.4Vx.4V.
0100000: eeac 0200 0010 0000 0000 0000 0000 0000  ................
0100010: 0000 1000 0000 0000 7ef5 0000 fc82 732e  ........~.....s.
0100020: 0100 0001 5175 cf0c 0819 950a 73ff 030b  ....Qu......s...
0100030: c173 be56 a8ba 274e 1234 5678 1234 5678  .s.V..'N.4Vx.4Vx
0100040: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0100050: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0100060: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0100070: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0100080: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
```
从上面的可以看出，第一行的最一个字节与第二行的第一个字符补改成了ee.

看报错的dump出来的数据

img.1048575.hdr_fail 这个文件只要第一个字节出错，后面的都是正确的，这里的不展示了。
```
[root@localhost ~]# xxd img.1048576.hdr_fail |head
0000000: eeac 0200 0010 0000 0000 0000 0000 0000  ................
0000010: 0000 1000 0000 0000 7ef5 0000 fc82 732e  ........~.....s.
0000020: 0100 0001 5175 cf0c 0819 950a 73ff 030b  ....Qu......s...
0000030: c173 be56 a8ba 274e 1234 5678 1234 5678  .s.V..'N.4Vx.4Vx
0000040: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000050: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000060: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000070: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000080: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000090: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
```

img.1044480.received为读取出来用于检验的数据，img.1044480.expected写入到文件的数据。
```
[root@localhost ~]# xxd  img.1044480.received |tail
0000f60: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000f70: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000f80: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000f90: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000fa0: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000fb0: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000fc0: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000fd0: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000fe0: 1234 5678 1234 5678 1234 5678 1234 5678  .4Vx.4Vx.4Vx.4Vx
0000ff0: 1234 5678 1234 5678 1234 5678 1234 56ee  .4Vx.4Vx.4Vx.4V.
```
img.1044480.received的最后一个字节，由于被改成了ee因为检验出错了。前面的verify_header也有一些不同，就不再细说了。
