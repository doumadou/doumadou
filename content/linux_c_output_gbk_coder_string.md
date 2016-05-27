---
layout: post
title: Linux c实现输出gbk编码的字符串
category: 练习
tags: [代码]
date: 2016-05-03 19:51:36
---

```
#include<stdio.h>
#include<string.h>

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

#include <iconv.h>

int code_convert(char *from_charset,char *to_charset,char *inbuf,int inlen,char *outbuf,int outlen)
{
		iconv_t cd;
		int rc;
		char **pin = &inbuf;
		char **pout = &outbuf;

		cd = iconv_open(to_charset,from_charset);
		if (cd==0)
				return -1;
		memset(outbuf,0,outlen);
		if (iconv(cd,pin,&inlen,pout,&outlen) == -1)
		{
			iconv_close(cd);
			return -1;
		}
		iconv_close(cd);
		return 0;
}

int u2g(char *inbuf,int inlen,char *outbuf,int outlen)
{
		return code_convert("utf-8","gb2312",inbuf,inlen,outbuf,outlen);
}

int g2u(char *inbuf,size_t inlen,char *outbuf,size_t outlen)
{
		return code_convert("gb2312","utf-8",inbuf,inlen,outbuf,outlen);
}

int main(int argc, char *argv[])
{
	int i = 0;
	char s[] = "本地连接";
	printf("GBK: %d\n", isgbk(s, strlen(s)));
	if (isgbk(s, strlen(s)) == 0)
	{
		char gbk[20] = {0};
		u2g(s, strlen(s), gbk, strlen(s));
		printf("str: %s\n", gbk);
	}
	return 0;
}

```
