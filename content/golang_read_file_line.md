Title: golang 按行读取文件
Category: golang
Tags: golang
Date: 2015-08-11 15:17:06
---


使用golang自带的bufio包，实现按行读取文件, 直接上源码


~~~golang
package main

import "fmt"
import "os"
import "io"
import "bufio"


func cat (r *bufio.Reader) {
	for {
		buf, err := r.ReadString('\n')
		if err == io.EOF {
			break
		}

		fmt.Println(buf)
	}
}

func main() {

	f, err := os.OpenFile("/proc/net/tcp", os.O_RDONLY, 0660)
	if err != nil {
		fmt.Println(err)
	}
	cat (bufio.NewReader(f))

	f.Close()
}

~~~
