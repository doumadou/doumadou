---
layout: post
title: Linux c判断字符串编码是否为gbk编码
category: c/c++
tags: [linux]
date: 2016-05-03 16:46:30
---

```
#include"stdint.h"
int isgbk(char *test , int n )
{
		if( n>2 &&(uint8_t)*test>=0x81 && (uint8_t)*test<=0xfe && ( ((uint8_t)*(test+1)>=0x80 && (uint8_t)*(test+1)<=0x7e) ||((uint8_t)*(test+1)>=0xa1 && (uint8_t)*(test+1)<=0xfe)))
		{
			return 1;
		}
		else
		{
			return 0;
		}
}

```
