---
layout: post
title: mingw编译win32 动态链接库dll
category: 
tags: []
date: 2017-03-29 14:36:46
---

```
//dlltest.c
int Double(int x)
{
    return x * 2;
}
```

```
//main.c
#include <stdio.h>
int Double(int x);
int main(void)
{
        printf("Hello :%d\n", Double(333));
	return 0;
}
```

Makefile
```
main.exe: main.c dlltest.dll
	x86_64-w64-mingw32-gcc $^ -o $@

dlltest.dll: dlltest.c
	x86_64-w64-mingw32-gcc $^ -shared -o $@ -Wl,--output-def,dlltest.def,--out-implib,dlltest.a
```
