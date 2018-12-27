---
layout: post
title: Linux内核源码中打印函数调用堆栈的方法dump_stack()
category: kernel
tags: [kernel]
date: 2018-12-27 10:25:52
---

 在linux内核调试中，经常用到的打印函数调用堆栈的方法非常简单，只需在需要查看堆栈的函数中加入：

dump_stack();或 __backtrace();即可。

 

dump_stack()在~/kernel/lib/Dump_stack.c中定义

```
void dump_stack(void)
{
 printk(KERN_NOTICE
  "This architecture does not implement dump_stack()/n");
}
```
__backtrace()的定义在~/kernel/arch/arm/lib/backtrace.S中

 
```
ENTRY(__backtrace)
  mov r1, #0x10
  mov r0, fp
```
 

在linux应用程序调试中，使用的方法是：

 

backtrace
backtrace_symbols

 

可以在函数中加入如下代码：
```
 void *bt[20]; 
 char **strings; 
 size_t sz;
 int i;

 sz = backtrace(bt, 20); 
 strings = backtrace_symbols(bt, sz); 
        for(i = 0; i < sz; ++i) 
                fprintf(stderr, "%s/n", strings[i]);
```
