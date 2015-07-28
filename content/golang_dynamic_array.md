Title: Golang动态数组
Date: 2015-07-28 10:20:40
Category: Golang 
Tags: Golang
Slug: golang-dynamic-array
Author: Gavin
Summary: golang use dynamic array
---

Golang使用动态数组


###数组申明


	var dynaArr []string

###动态添加成员


	dynaArr = append(dynaArr, "one")

###实例


	package main
	
	import  (
		"fmt"
	)
	
	func main() {
	
		var dynaArr []string
	
		dynaArr = append(dynaArr, "one")
		dynaArr = append(dynaArr, "two")
		dynaArr = append(dynaArr, "three")
	
		fmt.Println(dynaArr)
	}
	

###结构体数组

	package main
	
	import  (
		"fmt"
	)
	
	type A struct{
		Path	string
		Length  int	
	}
	
	
	func main() {
	
		var dynaArr []A
	
	
		t := A{"/tmp", 1023}
	
		dynaArr = append(dynaArr, t)
		dynaArr = append(dynaArr, A{"~", 2048})
		t.Path, t.Length = "/", 4096
		dynaArr = append(dynaArr, t)
	
		fmt.Println(dynaArr)
	}


注意大小写，大写为公有，小写为私有
