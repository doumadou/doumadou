Title: golang实现简单tcp端口转发功能
Category: golang
Tags: golang, 端口转发
Date: 2015-09-28 16:40:05
---

功能: 通过tcp端口转发功能实现通过777端口代理访问117.111.52.24的http服务。


~~~ golang
	package main
	
	import (
	    "fmt"
	    "io"
	    "net"
	    "os"
	)
	
	func main() {
	    host := "0.0.0.0"
	    port := "777"
	    l, err := net.Listen("tcp", fmt.Sprintf("%s:%s", host, port))
	    if err != nil {
	        fmt.Println(err, err.Error())
	        os.Exit(0)
	    }
	
	    for {
	        s_conn, err := l.Accept()
	        if err != nil {
	            continue
	        }
	
	        d_tcpAddr, _ := net.ResolveTCPAddr("tcp4", "117.111.52.24:80")
	        d_conn, err := net.DialTCP("tcp", nil, d_tcpAddr)
	        if err != nil {
	            fmt.Println(err)
	            s_conn.Write([]byte("can't connect 117.111.52.24:80"))
	            s_conn.Close()
	            continue
	        }
	        go io.Copy(s_conn, d_conn)
	        go io.Copy(d_conn, s_conn)
	    }
	}
~~~ 

代码实现说明:

本地监听777端口, 有tcp请求时，连接到117.111.52.24:80，开启二个协程，一个协程用于fd的读，一个协程序用于fd的写， io的重定向通过io.copy实现

io.Copy的功能，类似于将一个进程的标准输出重定向到另一个进程的标准输入。
io.Copy(dst Writer, src Reader) 
io.Copy(s_conn, d_conn) 从目标tcp链接fd中读取内容，写到源tcp链接fd中返回给客户端
io.Copy(d_conn, s_conn) 从接收到tcp链接fd中读取内容，写到目标tcp链接fd中,发往服务程序。


