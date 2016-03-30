---
layout: post
title: 打印strerror(errno)出现段错误
category: linux
tags: [Segmentation, strerror]
date: 2016-03-30 09:35:12
---


<pre>
#include <errno.h>  
#include <stdio.h>  
//#include <string.h>  
int main()  
{  
   FILE *fp = fopen("/etc/hosts", "a");  
   if(fp == NULL)  
   {  
     printf("%s\n", strerror(errno));  
   }  
}  

</pre>

编译运行出错：
Segmentation fault (core dumped)


原因由于没有加入strerror对应的头文件。所以编译时，出现警告，运行错误。 可以编译时的警告有时也是不能忽略的。

<pre>
#include <errno.h>  
#include <stdio.h>  
#include <string.h>  
int main()  
{  
   FILE *fp = fopen("/etc/hosts", "a");  
   if(fp == NULL)  
   {  
     printf("%s\n", strerror(errno));  
   }  
}  

</pre>

编译运行：
Permission denied

