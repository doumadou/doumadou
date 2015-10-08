Title: docker体验macvlan
Category: docker
Tags: docker, macvlan 
Date: 2015-10-08 17:05:34
---


docker所在的host初始化网络. 假设子网IP段为192.168.122.0/24, 网关为192.168.122.1, hostIP为192.168.122.77

###
    ip addr del 192.168.122.77/24 dev eth0
    ip link add link eth0 dev eth0m type macvlan mode bridge
    ip link set eth0m up
    ip addr add 192.168.122.77/24 dev eth0m
    route add default gw 192.168.122.1

###


1. 创建一个macvlan类型的虚拟网卡

ip link add link eth0 name macvlan0 type macvlan

2. 给macvlan0配置MAC

ip link set macvlan0 address 3a:46:0b:ca:bc:1b up

3. 创建netns
  a. 查看container pid 

  docker inspect jovial_lumiere |grep pid -i
        "Pid": 4330,
        "PidMode": "",

   b. 创建container netns链接(无此步骤，接下来没法操作), ip netns list将读取/var/run/netns文件夹。
    mkdir -vp /var/run/netns
	ln -s /proc/4330/ns/net /var/run/netns/4330

4. 将macvlan0置于namespace中

 ip link set macvlan0 netns 4430

5. 给macvlan0 调转IP 地址
	ip netns exec 4330 ifconfig macvlan0 192.168.122.101/24 up
6. 修改容器的默认网关。
    ip netns exec 4330 ip route replace default via 192.168.122.1



如果使用pipework一条命令就搞定了

###
    # pipework eth0 $container_name 192.168.122.234/24@192.168.122.1
###

