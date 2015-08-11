Title: Golang调用C/C++方法
Category: golang
Tags: Golang
Date: 2015-08-10 11:51:00
---


1. go文件中直接写c/c++代码，并调用

~~~golang
	package main  
	  
	/* 
	#include <stdio.h> 
	#include <stdlib.h> 
	#include <unistd.h> 
	void hello(const char *str)
	{
		printf("%s(%d): %s\n", __FUNCTION__, __LINE__, str);
	}
	*/  
	import "C"  
	  
	func main() {  
	  
	    C.hello(C.CString("call C hello func"))  
	}  
~~~

编译运行

	[root@localhost test]# go build main.go
	[root@localhost test]# ./main 
	hello(9): call C hello func


2. go调用c/c++动态库中的方法。

~~~bash
.
./hello.c
./hello.h
./main.go
~~~

hello.h

~~~c
#ifndef ___HELLO___
#define __HELLO___
void hello(const char *str);
#endif
~~~

hello.c

~~~c
#include "hello.h"
#include <stdio.h>

void hello(const char *str)
{
	printf("%s(%d): %s\n", __FUNCTION__, __LINE__, str);
}

~~~

main.go

~~~golang
package main  
  
/* 
#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include "hello.h" 
 
// intentionally write the same LDFLAGS differently 
#cgo linux LDFLAGS: -L. -lhello 
#cgo darwin LDFLAGS: -L. -lhello 
*/  
import "C"  
  
func main() {  
  
    C.hello(C.CString("call C hello func"))  
}  
~~~

编译运行:

	[root@localhost demo]# gcc -fPIC -shared hello.c -o libhello.so
	[root@localhost demo]# go build main.go
	[root@localhost demo]# ./main 
	hello(6): call C hello func
	[root@localhost demo]# 

3. go 使用线程库

仅修改hello.c文件

~~~c
[root@localhost demo1]# cat hello.c 
#include "hello.h"
#include <stdio.h>
#include <pthread.h>

void *func(void *arg)
{
	int i = 0;
	for (i = 0; i < 10; i++){
		printf("%d ", i);
	}
	printf("\n");
}

void hello(const char *str)
{
	pthread_t pthread;
	pthread_create(&pthread, NULL, &func, NULL);
	printf("%s(%d): %s\n", __FUNCTION__, __LINE__, str);
	pthread_join(pthread, NULL);
}
~~~

编译运行:

	[root@localhost demo1]# gcc -fPIC -shared hello.c -o libhello.so 
	[root@localhost demo1]# go build main.go
	[root@localhost demo1]# ./main 
	hello(18): call C hello func
	0 1 2 3 4 5 6 7 8 9 

