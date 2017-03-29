---
layout: post
title: Centos7.0交叉编译windows ffmpeg
category: 
tags: []
date: 2017-03-28 18:27:41
---

# 源码包
libtheora-1.1.1.tar.bz2
libvorbis-1.3.3.tar.gz
lame-3.99.5.tar.gz
libogg-1.3.1.tar.gz
xvidcore-1.3.4.tar.gz
speex-1.2.0.tar.gz
ffmpeg-3.2.4.tar.bz2
libopenjpeg.2.1.2.zip
libtheora-1.1.1
last_x264.tar.bz2
x264-snapshot-20170321-2245

http://ffmpeg.org/releases/ffmpeg-3.2.4.tar.bz2
https://nchc.dl.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
https://github.com/uclouvain/openjpeg/archive/v2.1.2.zip -O libopenjpeg.2.1.2.zip
http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz
http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.3.tar.gz
http://downloads.xiph.org/releases/ogg/libogg-1.3.1.tar.gz
http://downloads.xiph.org/releases/theora/libtheora-1.1.1.tar.bz2
ftp://ftp.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
http://downloads.xvid.org/downloads/xvidcore-1.3.4.tar.gz

# 编译

## x264
cd x264-snapshot-20170321-2245/

`build.sh`
```
SDK_DIR=/opt/build_ffmpeg
./configure --enable-static --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --cross-prefix=x86_64-w64-mingw32- --disable-asm
```

sh build.sh && make && make  install

## libogg

cd libogg-1.3.1/

`build.sh`

```
SDK_DIR=/opt/build_ffmpeg
./configure --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --enable-static --disable-shared
```
sh build.sh && make && make install

## lame

cd lame-3.99.5/

`build.sh`
```
 ./configure --host=x86_64-w64-mingw32 --prefix=/opt/build_ffmpeg --enable-static --disable-shared --disable-frontend
```

sh build.sh && make && make install

## speex

cd speex-1.2.0/

`build.sh`
```
SDK_DIR=/opt/build_ffmpeg
./configure --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --enable-static --disable-shared --disable-oggtest
```

sh build.sh && make && make install


## xvidcore

cd xvidcore/
cd build/generic/

`build.sh`
```
SDK_DIR=/opt/build_ffmpeg
./configure --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --disable-pthread

```
sh build.sh && make && make install

## libopenjpeg

cd openjpeg-2.1.2/
`build.sh`
```
SDK_DIR=/opt/build_ffmpeg
cmake -D CMAKE_TOOLCHAIN_FILE=../toolchain-windows.cmake -D CMAKE_INSTALL_PREFIX=${SDK_DIR}  .
```

`toolchain-windows.cmake`
```
SET(CMAKE_SYSTEM_NAME Windows)

SET(CMAKE_C_COMPILER   x86_64-w64-mingw32-gcc)
SET(CMAKE_CXX_COMPILER x86_64-w64-mingw32-g++)
SET(CMAKE_RC_COMPILER  x86_64-w64-mingw32-windres)

set(BUILD_SHARED_LIBS OFF)

SET(CMAKE_FIND_ROOT_PATH /usr/x86_64-w64-mingw32/sys-root/mingw)

SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)

SET(QT_QMAKE_EXECUTABLE /usr/x86_64-w64-mingw32/bin/qmake CACHE INTERNAL "" FORCE)
SET(QT_MOC_EXECUTABLE /usr/x86_64-w64-mingw32/bin/moc CACHE INTERNAL "" FORCE)
SET(QT_RCC_EXECUTABLE /usr/x86_64-w64-mingw32/bin/rcc CACHE INTERNAL "" FORCE)
SET(QT_UIC_EXECUTABLE /usr/x86_64-w64-mingw32/bin/uic CACHE INTERNAL "" FORCE)

```

sh build.sh && make && make install

## libvorbis

cd libvorbis-1.3.3/

build.sh
```
SDK_DIR=/opt/build_ffmpeg
./configure --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --enable-static --disable-shared --disable-oggtest
```
sh build.sh && make && make install

## libtheora

cd libtheora-1.1.1/
`build.sh`
```
SDK_DIR=/opt/build_ffmpeg
./configure --host=x86_64-w64-mingw32 --prefix=${SDK_DIR} --enable-static --disable-shared --disable-oggtest --disable-vorbistest --disable-sdltest --with-ogg-includes=${SDK_DIR}/include --with-ogg-libraries=${SDK_DIR}/lib
```
make && make install

## ffmpeg

与ffmpeg的源码同级目录创建一个用于build的文件夹，这里我创建一个build_ffmpeg文件夹
mkdir build_ffmpeg
cd build_ffmpeg/

`build.sh`
```
pkg_name=ffmpeg-3.2.4.tar.bz2
SDK_DIR=/opt/build_ffmpeg
export PKG_CONFIG_PATH=${SDK_DIR}/lib/pkgconfig/:${PKG_CONFIG_PATH}

../${pkg_name%%.tar.bz2}/configure --disable-static --enable-shared --enable-version3 --enable-gpl --enable-nonfree --disable-pthreads --enable-w32threads --enable-runtime-cpudetect --enable-memalign-hack --enable-libmp3lame --enable-libopenjpeg --enable-libspeex --enable-libtheora --enable-libvorbis --enable-libx264 --enable-libxvid --enable-zlib --enable-cross-compile --target-os=mingw32 --arch=x86 --prefix=${SDK_DIR}/ffmpeg --cross-prefix=x86_64-w64-mingw32- --extra-cflags="-I${SDK_DIR}/include" --extra-ldflags="-L${SDK_DIR}/lib" --disable-yasm

```
sh build.sh  && make && make install


以上编译成功之后，ffmpeg win32 sdk就出现在/opt/build_ffmpeg/ffmpeg里面了，bin目录下就是我们需要的所有文件了。


# 依赖文件
SDK /opt/build_ffmpeg/目录下的 bin/xvidcore.dll

zlib1.dll
libwinpthread-1.dll
iconv.dll
/usr/x86_64-w64-mingw32/sys-root/mingw/bin/iconv.dll
/usr/x86_64-w64-mingw32/sys-root/mingw/bin/zlib1.dll
/usr/x86_64-w64-mingw32/sys-root/mingw/bin/libwinpthread-1.dll
