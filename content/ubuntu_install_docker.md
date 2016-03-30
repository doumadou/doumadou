---
layout: post
title: ubuntu 安装最新版docker
category: linux
tags: [ubuntu, 安装docker]
date: 2016-03-30 09:39:15
---


1. 检查一下APT系统能够被https解析，如没有需要安装　apt-transport-https
　　sudo apt-get install apt-transport-https

2. 添加Docker repository key到本地keychain
　　sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
　　
3. sudo curl -sSL https://get.docker.com/ | sudo sh
