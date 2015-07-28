Title: Golang用for实现while
Date: 2015-07-28 14:10:32
Category: Golang 
Tags: Golang
Slug: golang-while
Author: Gavin
Summary: golang not while
---


Golang没有while关键词，所有用for实现while的功能。

很简单，将for二个;号两边的赋值去掉

例

	for ;; {
	}


实例如下

	package main
	
	import (
		"time"
	)
	
	func main() {
	
		for ;;{
		    print("====\n")
		    time.Sleep(1 * 1000 * 1000 *1000)
		}
	}


注意：time的Sleep方法中的单位为纳秒。
