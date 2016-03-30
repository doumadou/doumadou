Title: expect登陆linux执行ifconfig示例
Category: linux
Tags: linux, bash, expect
Date: 2015-10-09 17:32:13
---


1. 处理Permission denied, please try again.

2. timeout超时情况

3.  expect: spawn id exp7 not open 通过第一个expect的eof退出处理

~~~ bash
	#!/usr/bin/expect
	
	set VMIP [lindex $argv 0]
	set USER [lindex $argv 1]
	set PASS [lindex $argv 2]
	set timeout 20
	
	spawn ssh-keygen -R $VMIP
	spawn ssh $USER@$VMIP
	
	expect {
	eof { exit -1 }
	timeout { send_user "timeout\n"
			  exit -1
			}
	"Are you sure you want to continue connecting (yes/no)?" {send "yes\r"}
	"$USER@$VMIP's"
	}
	expect {
		"Permission denied, please try again." { 
			send_user "Permission denied, please try again.\n"
	        exit -1
		}
		"password:" {
			send "$PASS\n"
			exp_continue
		}
		"# " {
			send "ifconfig\r"
	        expect "# " { send "exit\r"
						exit 0
						}
		}
	}
~~~

