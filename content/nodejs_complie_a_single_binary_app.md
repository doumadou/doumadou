---
layout: post
title: 使用nexe将nodejs编译成一个独立可执行文件
category: nodejs
tags: [nodejs, nexe]
date: 2017-01-16 15:09:36
---

使用nexe编译nodejs文件，有二种方法；

第一种: 安装nexe

安装nexe
```
yum install npm
npm install nexe
```

编译文件
```
./node_modules/nexe/bin/nexe  -i input.js -o input # 第一次执行时，该命令会下载最新版的nodejs,并编译，因此时间会比较久。
```

第二种：使用docker-nexe镜像编译


前提：需要安装docker

下载docker镜像
```
# sudo docker pull asbjornenge/nexe-docker
```

运行docker编译 nodejs (--rm 参数表示，使用编译完成后，删除该窗器)
```
# docker run -v $(pwd):/app --rm -w /app asbjornenge/nexe-docker -i input.js -o app.bin
```

限制：

1.  不支持动态加载模块

例如函数中使用
```
  var base58 = require(__dirname+'/base58.js')({ sjcl: options.sjcl });;
  var MasterKey = require(__dirname+'/master_key.js')({ sjcl: options.sjcl });
  var RippleAddress = require(__dirname+'/ripple_address.js')({ sjcl: options.sjcl });
  var PublicGenerator = require(__dirname+'/public_generator.js')({ sjcl: options.sjcl });

```
则需要进行修改才能支持编译成exe

下面是修改方案
```
[root@192-168-230-152 ~]# diff /tmp/node_modules/ripple-wallet-generator/lib/wallet.js ./node_modules/ripple-lib/node_modules/ripple-wallet-generator/lib/wallet.js
0a1,4
> var base58 = require('./base58.js');
> var MasterKey = require('./master_key.js');
> var RippleAddress = require('./ripple_address.js');
> var PublicGenerator = require('./public_generator.js');
4a9
> /*
8a14,19
> */
>   base58.sjcl = options.sjcl;
>   MasterKey.sjcl = options.sjcl;
>   RippleAddress.sjcl =  options.sjcl;
>   PublicGenerator.sjcl = options.sjcl;
> 
```
