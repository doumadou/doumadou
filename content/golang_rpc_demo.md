Title: Golang使用RPC
Category: golang 
Tags: golang, rpc
Date: 2015-08-10 17:17:32
---


使用golang自带的rpc和http包


##服务端

~~~golang

package main

import (
	"fmt"
	"net"
	"net/http"
	"net/rpc"
)


type Watcher int

func (w *Watcher) AddInfo(info string, result *int) error {
	*result = 1
	fmt.Println("Add: " + info)
	return nil
}


func main() {

	watcher := new(Watcher)

	rpc.Register(watcher)

	rpc.HandleHTTP()

	l, err := net.Listen("tcp", ":8080")
	if err != nil {
		fmt.Println("listent tcp port failed!")
	}

	fmt.Println("listening 0.0.0.0:8080")

	http.Serve(l, nil)
}

~~~


##客户端

~~~golang
package main


import (
	"fmt"
	"net/rpc"
)


func main() {
	client, err := rpc.DialHTTP("tcp", "127.0.0.1:8080")
	if err != nil {
		fmt.Println("connect rpc server failed:", err);
	}

	var ret int
	err = client.Call("Watcher.AddInfo", "http://doumadou.github.io", &ret)
	if err != nil {
		fmt.Println("RPC call failed", err)
	}

	fmt.Println("RPC ret value:", ret)
}

~~~


运行结果:

	[root@localhost demo_rpc]# go run server.go 
	listening 0.0.0.0:8080
	Add: http://doumadou.github.io
	Add: http://doumadou.github.io
	
	
	[root@localhost demo_rpc]# go run client.go
	RPC ret value: 1
	[root@localhost demo_rpc]# go run client.go
	RPC ret value: 1

