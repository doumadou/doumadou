---
layout: post
title: Centos7交叉编译windows c++的socket.io client
category: c++
tags: []
date: 2017-06-23 16:48:24
---

c++ socket.io client
```
https://github.com/socketio/socket.io-client-cpp.git
```

## 安装依赖:
openssl, boost
```
# yum install mingw64-openssl
# yum install -y mingw64-boost
```
## 修改openssl头文件
/usr/x86_64-w64-mingw32/sys-root/mingw/include/openssl/opensslv.h
```
#define OPENSSL_VERSION_NUMBER  0x1000208fL
```
(#与define)中的空格去掉

## 修改源码
1. 修改使用低版本的cmake
```
# sed -i -e 's/cmake_minimum_required(VERSION 3.1.0/cmake_minimum_required(VERSION 2.8.12/' ./CMakeLists.txt
```
2. 修改使用低版本的boost(boost版本根据yum install 安装mingw64-boost后的版本确定)

CMakeLists.txt
```
set(BOOST_VER "1.54.0" CACHE STRING "boost version" )
```

## 编译

toolchain-windows.cmake
```
SET(CMAKE_SYSTEM_NAME Windows)

SET(CMAKE_C_COMPILER   x86_64-w64-mingw32-gcc)
SET(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
#SET(CMAKE_CXX_CFLAGS -std=c++11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
SET(CMAKE_RC_COMPILER  x86_64-w64-mingw32-windres)

set(BUILD_SHARED_LIBS OFF)

SET(CMAKE_FIND_ROOT_PATH /usr/x86_64-w64-mingw32/sys-root/mingw)

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

```

编译
```
# cmake -D CMAKE_TOOLCHAIN_FILE=../toolchain-windows.cmake  .
# make
```

编译完成后，生成二个静态库
`libsioclient.a`和`libsioclient_tls.a`


## domo:

```
# x86_64-w64-mingw32-g++ -std=c++11 -D__STDC_CONSTANT_MACROS -g main.cpp -o main -L./ -lsioclient -lsioclient_tls -lboost_system -lwsock32 -lws2_32
```

undefined reference to `__imp_freeaddrinfo'  ----> lws2_32

undefined reference to `__imp_WSAStartup' undefined reference to `__imp_WSACleanup'  ----> lwsock32
