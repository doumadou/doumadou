Title: golang实现简单http文件服务器
Category: golang
Tags: golang
Date: 2015-08-24 16:00:01
---


golang实现简单http文件服务器 类似python -m SimpleHTTPServer

~~~golang
package main

import (
	"fmt"
	"net/http"
)

func main() {
	http.Handle("/", http.FileServer(http.Dir(".")))
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		fmt.Println("ListenAndServe: ", err)
	}
}

~~~
