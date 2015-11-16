Title: 二台服务利用ssh边压缩边传输
Categories: linux
Tags: scp
Date: 2015-10-20 10:36:39
---



tar czf - /var/log/ |ssh root@192.168.122.4 "cat > log.tar.bz2"
