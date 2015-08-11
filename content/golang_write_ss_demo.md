Title: golang 实现ss/netstat
Category: golang 
Tags: golang, netstat, ss
Date: 2015-08-11 16:40:13
---

今天遇到一个问题。 使用netstat命令查看, 发现tcp某链接长时间处于CLOST_WAIT状态。所以想看看netstat是如些实现的。直接下载netstat源码看实现。netstat主要是读/proc/net/下的文件。而当时host是/proc文件已经阻塞。ls命令都会被阻塞。因此这才是导致TCP链接状态长期不更新的原因。

正在学golang于是go实现类似ss, netstat命令的功能。直接上代码



~~~golang

package main


import (
	"fmt"
	"os"
	"bufio"
	"io"
	"strings"
	"strconv"
)

func load_data() []string {

	var str []string

	tcpFile := "/proc/net/tcp"

	fin, err := os.Open(tcpFile)

	defer fin.Close()

	if err != nil {
		fmt.Println(tcpFile, err)
		return str
	}

	r := bufio.NewReader(fin)

	for {
		buf, err := r.ReadString('\n')
		if err == io.EOF { break }
		str = append(str, buf)
	}
	
	if len(str) > 0 {
		return str[1:]
	}
	return str
}

func hex2dec(hexstr string) string{
	i, _ := strconv.ParseInt(hexstr, 16, 0)
	return strconv.FormatInt(i, 10)
}

func hex_to_ip(hexstr string) (string, string) {
	var ip string
	if len(hexstr) != 8 {
		err := "parse error"
		return ip, err
	}

	i1, _ := strconv.ParseInt(hexstr[6:8], 16, 0)
	i2, _ := strconv.ParseInt(hexstr[4:6], 16, 0)
	i3, _ := strconv.ParseInt(hexstr[2:4], 16, 0)
	i4, _ := strconv.ParseInt(hexstr[0:2], 16, 0)
	ip = fmt.Sprintf("%d.%d.%d.%d", i1, i2, i3, i4)

	return ip, ""
}

func convert_to_ip_port(str string) (string, string) {
	l := strings.Split(str, ":")
	if len(l) != 2 {
		return str, ""
	}

	ip, err := hex_to_ip(l[0])
	if err != "" {
		return str, ""
	}

	return ip, hex2dec(l[1])
}

func remove_all_space(l [] string) [] string {
	var ll []string
	for _, v := range l {
		if v != "" {
			ll = append(ll, v)
		}
	}

	return ll
}

var STATE = map[string]string{
				"01":"ESTABLISHED",
				"02":"SYN_SENT",
				"03":"SYN_RECV",
				"04":"FIN_WAIT1",
				"05":"FIN_WAIT2",
				"06":"TIME_WAIT",
				"07":"CLOSE",
				"08":"CLOSE_WAIT",
				"09":"LAST_ACK",
				"0A":"LISTEN",
				"0B":"CLOSING",
				}


func main() {
	fmt.Println("ss demo use golang");

	lines := load_data()

	fmt.Printf("State\tLocal Address:Port\t\t\tPeer Address:Port\n")
	for _, line := range lines {
		//fmt.Println(line)
		l := remove_all_space(strings.Split(line, " "))
		l_host, l_port := convert_to_ip_port(l[1])
		r_host, r_port := convert_to_ip_port(l[2])
		stats := STATE[l[3]]
		fmt.Printf("%s\t\t%s:%s\t\t\t%s:%s\n", stats, l_host, l_port, r_host, r_port)
	}
}


~~~
