---
layout: post
title: linux搭建gtest开发环境
category: linux
tags: [linux, gtest]
date: 2016-03-30 09:38:09
---

linux搭建gtest开发环境

gtest版本 gtest-1.7.0

编译

cd gtest-1.7.0/make && make

生成  sample1_unittestt 和 gtest_main.a
$ ./sample1_unittest 
Running main() from gtest_main.cc
[==========] Running 6 tests from 2 test cases.
[----------] Global test environment set-up.
[----------] 3 tests from FactorialTest
[ RUN      ] FactorialTest.Negative
[       OK ] FactorialTest.Negative (0 ms)
[ RUN      ] FactorialTest.Zero
[       OK ] FactorialTest.Zero (0 ms)
[ RUN      ] FactorialTest.Positive
[       OK ] FactorialTest.Positive (0 ms)
[----------] 3 tests from FactorialTest (0 ms total)

[----------] 3 tests from IsPrimeTest
[ RUN      ] IsPrimeTest.Negative
[       OK ] IsPrimeTest.Negative (0 ms)
[ RUN      ] IsPrimeTest.Trivial
[       OK ] IsPrimeTest.Trivial (0 ms)
[ RUN      ] IsPrimeTest.Positive
[       OK ] IsPrimeTest.Positive (0 ms)
[----------] 3 tests from IsPrimeTest (0 ms total)

[----------] Global test environment tear-down
[==========] 6 tests from 2 test cases ran. (0 ms total)
[  PASSED  ] 6 tests.


写自己的测试用例
创建文件
mkdir test

复制gtest静态库
cp gtest-1.7.0/make/gtest_main.a test/libgtest.a

测试用例文件 test_1.cpp
<pre>
#include <iostream>  
#include <gtest/gtest.h>  
  
using namespace std;  
  
int Foo(int a,int b)  
{  
 return a+b;  
}  
  
TEST(FooTest, ZeroEqual)  
{  
 ASSERT_EQ(0,0);  
}  
  
TEST(FooTest, HandleNoneZeroInput)  
{  
    EXPECT_EQ(6, Foo(2, 4));  
    EXPECT_EQ(12,Foo(4, 10));  
}  
</pre>

创建Makefile
<pre>
TARGET=test_1
GTEST_DIR = /tmp/gtest-1.7.0

CPPFLAGS += -I$(GTEST_DIR)/include -L./ -lgtest -lpthread
  
all:  
	g++ $(CPPFLAGS)  -o $(TARGET).o -c test_1.cpp  
	g++ $(CPPFLAGS) -o $(TARGET) $(TARGET).o  
clean:  
	rm -rf *.o $(TARGET) 
</pre>

编译:
	$ make

运行测试用例：
	$ ./test_1
	
运行指定测试用例:
	./test_1 --gtest_filter=FooTest.ZeroEqual
	
运行指定多个测试用例:(:分隔)
	./test_1 --gtest_filter=FooTest.ZeroEqual:FooTest.HandleNoneZeroInput

列出所有测试用例:
	./test_1 --gtest_list_tests
Running main() from gtest_main.cc
FooTest.
  ZeroEqual
  HandleNoneZeroInput

