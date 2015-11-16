Title: docker动态映射窗器内部端口
由docker动态映射端口引发的思考
Category: docker 
Tags: iptables, docker 
Date: 2015-09-28 13:43:00
---


##使用iptables 动态映射端口

没做映射之前测试：

container里开启的httpServer服务。container的IP地址为 172.17.0.12

docker所在host运行wget(host并没有运行开启80端口的任何服务)
~~~shell
root@vultr:~ # wget 127.0.0.1
--2015-09-28 05:46:43--  http://127.0.0.1/
Connecting to 127.0.0.1:80... failed: Connection refused.
~~~

通过container的IP地址访问服务

~~~shell
root@vultr:~ # wget 172.17.0.12
--2015-09-28 05:46:33--  http://172.17.0.12/
Connecting to 172.17.0.12:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

    [ <=>                                                                                                                 ] 7,379       --.-K/s   in 0s      
2015-09-28 05:46:33 (62.8 MB/s) - ‘index.html’ saved [7379]
~~~

使用iptables映射窗器内的80端口

~~~shell
# /sbin/iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to 172.17.0.12:80
~~~

做映射之后测试：

container里开启的httpServer服务。container的IP地址为 172.17.0.12

docker所在host运行wget(host并没有运行开启80端口的任何服务)
~~~shell
root@vultr:~ # wget 127.0.0.1
[root@testnode tmp]# wget http://107.191.52.64/
--2015-09-28 14:17:33--  http://107.191.52.64/
Connecting to 107.191.52.64:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: “index.html.1”

    [ <=>                                                                                                                 ] 7,379       --.-K/s   in 0s      

2015-09-28 14:17:33 (281 MB/s) - “index.html.1” saved [7379]

~~~

通过container的IP地址访问服务

~~~shell
root@vultr:~ # wget 172.17.0.12
--2015-09-28 05:46:33--  http://172.17.0.12/
Connecting to 172.17.0.12:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Saving to: ‘index.html’

    [ <=>                                                                                                                 ] 7,379       --.-K/s   in 0s      
2015-09-28 05:46:33 (62.8 MB/s) - ‘index.html’ saved [7379]
~~~


##iptables 命令详解












========================================================================================================\n

# docker run -d -p 80:80 images
f0c4aee1b164872ec45c866b477cca2b249b2251a854ecded34620792d1198ec

# wget 127.0.0.1
--2015-09-28 07:29:26--  http://127.0.0.1/
Connecting to 127.0.0.1:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: ‘index.html’

100%[====================================================================================================================>] 15          --.-K/s   in 0s      
2015-09-28 07:29:26 (3.33 MB/s) - ‘index.html’ saved [15/15]

# netstat -npa |grep 80 -w
tcp6       0      0 :::80                   :::*                    LISTEN      14478/docker-proxy

# ps -ef |grep 14478
root     14478   729  0 07:29 ?        00:00:00 docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 80 -container-ip 172.17.0.13 -container-port 80

# kill -9 14478

#  wget 127.0.0.1
--2015-09-28 07:41:09--  http://127.0.0.1/
Connecting to 127.0.0.1:80... failed: Connection refused.

歇菜了。。。。

外网访问， 仍然OK

# wget http://107.191.52.64/
--2015-09-28 15:46:07--  http://107.191.52.64/
Connecting to 107.191.52.64:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: “index.html”

100%[====================================================================================================================>] 15          --.-K/s   in 0s      

2015-09-28 15:46:08 (1.79 MB/s) - “index.html” saved [15/15]


再次实验保留docker-proxy,进程，清空iptables.

猜想iptables并没有什么用，真正起作用的应该是docker-proxy进程。

# docker run -d -p 80:80 contest.csphere.cn/604569659-qq-com/http-server
ad3e33f7b38e3da54c810eaefde56cda6cc5a08024b4a32e2a7ce5b5bf365d36

清空iptables里的相关规则(/sbin/iptables -t nat -D DOCKER 1)

内网访问：正常
# wget 127.0.0.1
--2015-09-28 07:58:13--  http://127.0.0.1/
Connecting to 127.0.0.1:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: ‘index.html’

100%[====================================================================================================================>] 15          --.-K/s   in 0s      

2015-09-28 07:58:13 (3.11 MB/s) - ‘index.html’ saved [15/15]

外网访问：正常
# wget http://107.191.52.64/
--2015-09-28 16:02:17--  http://107.191.52.64/
Connecting to 107.191.52.64:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: “index.html.1”

100%[====================================================================================================================>] 15          --.-K/s   in 0s      

2015-09-28 16:02:17 (1.94 MB/s) - “index.html.1” saved [15/15]


用go实现一个类似docker-proxy tcp转发功能的程序my_docker_proxy。代码见文章最后。

末映射端口
root@vultr:~# docker run -d contest.csphere.cn/604569659-qq-com/http-server
8f80d09f4715176e6e38aa8f43f2c813954c2cdf585f941380ef1502488f814e
root@vultr:~# wget 127.0.0.1
--2015-09-28 09:28:19--  http://127.0.0.1/
Connecting to 127.0.0.1:80... failed: Connection refused.
获取contiainer IP
root@vultr:~# docker inspect --format '{{.NetworkSettings.IPAddress}}' 8f80d09f4715176e6e38aa8f43f2c813954c2cdf585f941380ef1502488f814e
172.17.0.15

使用my_docker_proxy作动态端口映射
root@vultr:~# ./my_docker_proxy  -host-port 80 -container-ip 172.17.0.15 -container-port 80 

内网访问：OK
root@vultr:~# wget 127.0.0.1
--2015-09-28 09:32:34--  http://127.0.0.1/
Connecting to 127.0.0.1:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: ‘index.html.1’

100%[====================================================================================================================>] 15          --.-K/s   in 0s      

2015-09-28 09:32:34 (3.11 MB/s) - ‘index.html.1’ saved [15/15]


外网访问：OK
# wget http://107.191.52.64/
--2015-09-28 17:35:40--  http://107.191.52.64/
Connecting to 107.191.52.64:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 15
Saving to: “index.html”

100%[====================================================================================================================>] 15          --.-K/s   in 0s      
2015-09-28 17:35:40 (1.44 MB/s) - “index.html” saved [15/15]

my_docker_proxy.go源代码

~~~golang
package main

import (
    "fmt"
	"flag"
    "io"
    "net"
    "os"
)

func main() {
    host := flag.String("host-ip", "0.0.0.0", "src ip")
    port := flag.String("host-port", "", "src port")
	container_ip := flag.String("container-ip", "", "container ip")
	container_port := flag.String("container-port", "", "container port")
    flag.Parse()
	fmt.Println(*host, *port, *container_ip, *container_port)
	if *port == "" || *container_port == "" || *container_ip == "" {
		fmt.Println("usage: [-host-ip <>] -host-port <> -container-ip <> -container-port <>")
		os.Exit(-1)
	}
    l, err := net.Listen("tcp", fmt.Sprintf("%s:%s", *host, *port))
    if err != nil {
        fmt.Println(err, err.Error())
        os.Exit(-1)
    }

    for {
        s_conn, err := l.Accept()
        if err != nil {
            continue
        }

        d_tcpAddr, _ := net.ResolveTCPAddr("tcp4", fmt.Sprintf("%s:%s", *container_ip, *container_port))
        d_conn, err := net.DialTCP("tcp", nil, d_tcpAddr)
        if err != nil {
            fmt.Println(err)
            s_conn.Write([]byte(err.Error()))
            s_conn.Close()
            continue
        }
        go io.Copy(s_conn, d_conn)
        go io.Copy(d_conn, s_conn)
    }
}

~~~

以上代码有个问题，当httpserver不返回Content-Length时，client一直不结束.

proxy与server的连接状态，一直处于close_wait状态。proxy与client的状态一直处理ESTABLISHED状态, FIN_WAIT2一段时间后会退出
 ./my_docker_proxy -host-port 8000  -container-ip 127.0.0.1 -container-port 8001
[root@testnode ~]# netstat -npa |grep 8001
tcp        0      0 127.0.0.1:8001              0.0.0.0:*                   LISTEN      13736/python        
tcp        0      0 127.0.0.1:8001              127.0.0.1:41384             FIN_WAIT2   -                   
tcp        0      0 127.0.0.1:41384             127.0.0.1:8001              CLOSE_WAIT  13738/./my_docker_p 
[root@testnode ~]# netstat -npa |grep 8000
tcp        0      0 :::8000                     :::*                        LISTEN      13738/./my_docker_p 
tcp        0      0 ::ffff:192.168.122.77:8000  ::ffff:192.168.122.1:60200  ESTABLISHED 13738/./my_docker_p


梁Content-Length有值里，client退出。但是proxy的socket status 一直处理CLOSE_WAITE
[root@testnode ~]# netstat -npa |grep 8001
tcp        0      0 127.0.0.1:41390             127.0.0.1:8001              CLOSE_WAIT  13959/./my_docker_p 
tcp        0      0 127.0.0.1:41389             127.0.0.1:8001              CLOSE_WAIT  13959/./my_docker_p 
[root@testnode ~]# netstat -npa |grep 8000
tcp        0      0 :::8000                     :::*                        LISTEN      13959/./my_docker_p 
tcp        0      0 ::ffff:192.168.122.77:8000  ::ffff:192.168.122.1:60584  CLOSE_WAIT  13959/./my_docker_p 
tcp        0      0 ::ffff:192.168.122.77:8000  ::ffff:192.168.122.1:60579  CLOSE_WAIT  13959/./my_docker_p 


CLOSE_WAIT:造成的原因，作类被被动方，收到FIN，but not send FIN to peer.

有Content-Length, client close, http-server send auto close. so proxy allways beclosed peer.
