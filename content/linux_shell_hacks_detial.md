---
layout: post
title: Linux shell hacks
category: Linux
tags: [shell]
date: 2016-06-30 10:13:30
---

# 环境变量
## PS1
```
[root@a71641d705a7 test]# export PS1="[\u@doumadou.github.io \W]# "
[root@doumadou.github.io test]# 
```
说明:

`\u`: 当前用户名
`\h`: 当前hostname
`\w`: 全路径
`\W`: 当前目录名
`\t`:  to display the current time in the hh:mm:ss
`\@`: to display the current time in 12-hour am/pm eg: 04:12 PM
`\!`: The history number of the command
`$kernel_version`: The output of the uname -r command from $kernel_version variable
`\$?`: Status of the last command

### PS1 prompt带前景色

```
export PS1="\e[0;31m[\u@doumadou.github.io \W]# \e[m"
```

```
    \e[ – Indicates the beginning of color prompt
    x;ym – Indicates color code. Use the color code values mentioned below.
    \e[m – indicates the end of color prompt

Color Code Table:

    Black 0;30
    Blue 0;34
    Green 0;32
    Cyan 0;36
    Red 0;31
    Purple 0;35
    Brown 0;33

[Note: Replace 0 with 1 for dark color]
```

### PS1 prompt带背景色
```
export PS1="\e[43m\e[34m[\u@doumadou.github.io \W]# \e[m"
Play around by using the following background color and choose the one that match your taste:

    \e[40m
    \e[41m
    \e[42m
    \e[43m
    \e[44m
    \e[45m
    \e[46m
    \e[47m
```


## PROMPT_COMMAND

PROMPT_COMMAND 的内容显示到 PS1内容前。
```
[root@doumadou.github.io tmp]# 
[root@doumadou.github.io tmp]# export PROMPT_COMMAND="date +%H:%M:%S"
07:14:10
[root@doumadou.github.io tmp]#
```
有换行符，可以使用`echo -n`
```
[root@doumadou.github.io tmp]# 
07:17:10
[root@doumadou.github.io tmp]# export PROMPT_COMMAND="echo -n [$(date +%H:%M:%S)]"
[07:17:20][root@doumadou.github.io tmp]# 
[07:17:20][root@doumadou.github.io tmp]# 
```


## CDPATH

CDPATH环境变量的语法，作用与PATH类似；

CDPATH指定cd切换路径时，查找路径。 配置这个变量后，能大大提高cd时的效率。

```
[root@doumadou.github.io test]# cd /tmp
[root@doumadou.github.io tmp]# ls
test test.sql
[root@doumadou.github.io tmp]# export CDPATH=.:/var
[root@doumadou.github.io tmp]# pwd
/tmp
[root@doumadou.github.io tmp]# cd log
/var/log
[root@doumadou.github.io log]# pwd
/var/log
```
## 将mkdir和cd合并成一条命令

我们经常有这样的需求, 创建一个目录，然后切换到这个目录下。
以前我们是这样做的
```
[root@doumadou.github.io ~]# mkdir /tmp/aa/bb/cc/dd -vp
mkdir: created directory '/tmp/aa'
mkdir: created directory '/tmp/aa/bb'
mkdir: created directory '/tmp/aa/bb/cc'
mkdir: created directory '/tmp/aa/bb/cc/dd'
[root@doumadou.github.io ~]# cd /tmp/aa/bb/cc/dd
[root@doumadou.github.io dd]# pwd
/tmp/aa/bb/cc/dd
[root@doumadou.github.io dd]# 
```
如果将mkdir 和cd作为一条命令是不是更方便?　有人肯定会说 `mkdir -vp *** && cd ***` (一样的麻烦)；`path=***;mkdir -vp $path && cd $path` (也麻烦)

Linux没有这样的命令我们就自己创建一个这样的命令，编辑 ~/.bash_profile 加入`function mkdircd() { mkdir -p "$@" && eval cd "\"\$$#\""; }`
```
[root@doumadou.github.io ~]# cat ~/.bash_profile 
# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
	. ~/.bashrc
fi

# User specific environment and startup programs

PATH=$PATH:$HOME/bin

export PATH

function mkdircd() { mkdir -p "$@" && eval cd "\"\$$#\""; }
[root@doumadou.github.io ~]# source ~/.bash_profile 
[root@doumadou.github.io ~]# rm /tmp/aa/ -rv
rm: descend into directory '/tmp/aa/'? ^C
[root@doumadou.github.io ~]# rm -rf /tmp/aa/    
[root@doumadou.github.io ~]# mkdircd /tmp/aa/bb/cc/dd
[root@doumadou.github.io dd]# pwd
/tmp/aa/bb/cc/dd
[root@doumadou.github.io dd]# 
```

## history

同一账号同时多次登录写入history

普通情况下， 当以bash登录系统时，系统会从~/.bash_history读取以前运行的命令 当注销时，把最新的1000（HISTSIZE）条命令更新到~/.bash_history文件中。 也可以使用history -w强制立刻写入，仅保留最新的。
当同一账号，同时登录多个bash时，只有最后一个退出的会写入bash_history,其他的都被覆盖了。

### history记录的行数
HISTSIZE=1000
不想让shell记录历史命令，可以将该值设为0.

### history命令显示时间，history是默认不带时间
HISTTIMEFORMAT="%F %T "
```
[07:17:20][root@doumadou.github.io tmp]# echo $HISTTIMEFORMAT
%F %T
[07:17:20][root@doumadou.github.io tmp]# history 2 
   28  2016-07-01 03:02:16 history -2
   29  2016-07-01 03:02:18 history 2
```

### 在历史命令中查找
`Ctrl+r`　然后输入关键词即可查找.

### 重复执行上一条命令
* up/down key
* `!!`
* `!-1`, 1 也可以改为其它值，表示前N条命令
上面二种方式的优点是简单方便，缺点是运行前不能看到命令。
* `Ctrl+P`

### 运行history中特定的命令
```
[07:17:20][root@doumadou.github.io tmp]# history 10
   40  2016-07-01 03:14:43 pwd
   41  2016-07-01 03:14:51 ps -ef |grep pwd
   42  2016-07-01 03:14:56 pwd
   43  2016-07-01 03:15:44 pwd
   44  2016-07-01 03:19:01 history | more
   45  2016-07-01 03:19:11 vim ~/.bashrc 
   46  2016-07-01 03:19:18 history | more
   47  2016-07-01 03:19:25 history 10
   48  2016-07-01 03:19:38 time
   49  2016-07-01 03:19:41 history 10
```
比如想运行 48 行的`time`命令。 输入`!48` 即可。

`! + 历史命令中开始的几字符`也可执行相应的命令
### 历史命令文件名
`HISTFILE`

### HISTCONTROL

HISTCONTROL=ignoredups 清除连续重复的命令
```
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# echo $HISTCONTROL

[07:17:20][root@doumadou.github.io tmp]# history  4
   67  2016-07-01 03:50:40 pwd
   68  2016-07-01 03:50:42 pwd
   69  2016-07-01 03:50:45 echo $HISTCONTROL
   70  2016-07-01 03:50:49 history  4
```

```
[07:17:20][root@doumadou.github.io tmp]# HISTCONTROL=ignoredups
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# history 4
   76  2016-07-01 03:52:10 pw
   77  2016-07-01 03:52:13 HISTCONTROL=ignoredups
   78  2016-07-01 03:52:15 pwd
   79  2016-07-01 03:52:21 history 4
```

HISTCONTROL=erasedups 消除整个历史中重复的命令
```
[07:17:20][root@doumadou.github.io tmp]# history 4
   76  2016-07-01 03:52:10 pw
   77  2016-07-01 03:52:13 HISTCONTROL=ignoredups
   78  2016-07-01 03:52:15 pwd
   79  2016-07-01 03:52:21 history 4
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# history 4
   78  2016-07-01 03:52:15 pwd
   79  2016-07-01 03:52:21 history 4
   80  2016-07-01 03:55:57 pwd
   81  2016-07-01 03:56:01 history 4
[07:17:20][root@doumadou.github.io tmp]# HISTCONTROL=erasedups
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# history 4
   67  2016-07-01 03:52:13 HISTCONTROL=ignoredups
   68  2016-07-01 03:56:30 HISTCONTROL=erasedups
   69  2016-07-01 03:56:31 pwd
   70  2016-07-01 03:56:36 history 4
```

HISTCONTROL=ignorespace 强制histroy不记录特定的命令, 不记录命令前面以空白符开头的命令。
```
[07:17:20][root@doumadou.github.io tmp]# HISTCONTROL=ignorespace
[07:17:20][root@doumadou.github.io tmp]# pwd
/tmp
[07:17:20][root@doumadou.github.io tmp]# history 4
   70  2016-07-01 03:56:36 history 4
   71  2016-07-01 05:20:10 HISTCONTROL=ignorespace
   72  2016-07-01 05:20:15 pwd
   73  2016-07-01 05:20:18 history 4
[07:17:20][root@doumadou.github.io tmp]#  time     

real	0m0.000s
user	0m0.000s
sys	0m0.000s
[07:17:20][root@doumadou.github.io tmp]# history 4
   71  2016-07-01 05:20:10 HISTCONTROL=ignorespace
   72  2016-07-01 05:20:15 pwd
   73  2016-07-01 05:20:18 history 4
   74  2016-07-01 05:20:36 history 4

```

替换histroy命令中的词. `!^` 获取上一条命令的第一个参数, `!$`获取上一条命令的最后一个参数。
```
[07:17:20][root@doumadou.github.io tmp]# cat test1.txt test2.txt
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
aa $5,000
ab $500
ac $3,000
ad $1,250
[07:17:20][root@doumadou.github.io tmp]# ls -ltr !^
ls -ltr test1.txt
-rw-r--r-- 1 root root 63 Jun 30 06:44 test1.txt
```

通过HISTIGNORE配置某些命令将不被保存到历史记录中

HISTIGNORE="pwd:ls:ls –ltr:"
```
[07:17:20][root@doumadou.github.io ~]# HISTIGNORE="pwd:ls:ls -ltr:"
[07:17:20][root@doumadou.github.io ~]# pwd
/root
[07:17:20][root@doumadou.github.io ~]# ls
11.sql  mysql  test
[07:17:20][root@doumadou.github.io ~]# ls -ltr
total 560
drwxr-x--- 2 mysql root   4096 Jun 15 08:25 test
drwxr-x--- 2 mysql root   4096 Jun 15 08:30 mysql
-rw-r--r-- 1 root  root 563580 Jun 22 01:57 11.sql
[07:17:20][root@doumadou.github.io ~]# ls -l
total 560
-rw-r--r-- 1 root  root 563580 Jun 22 01:57 11.sql
drwxr-x--- 2 mysql root   4096 Jun 15 08:30 mysql
drwxr-x--- 2 mysql root   4096 Jun 15 08:25 test
[07:17:20][root@doumadou.github.io ~]# history 6 
  167  2016-07-01 06:48:44 history 
  168  2016-07-01 06:48:46 clear
  169  2016-07-01 06:48:49 HISTIGNORE="pwd:ls:ls -ltr:"
  170  2016-07-01 06:48:57 ls -l
  171  2016-07-01 06:49:06 history 6
```


# 命令

## dirs/pushd/popd
```
[root@doumadou.github.io tmp]# find aa/
aa/
aa/bb
aa/bb/cc
aa/bb/cc/dd
[root@doumadou.github.io tmp]# dirs
/tmp
[root@doumadou.github.io tmp]# pushd aa/
/tmp/aa
/tmp/aa /tmp
[root@doumadou.github.io aa]# dirs
/tmp/aa /tmp
[root@doumadou.github.io aa]# pushd bb
/tmp/aa/bb
/tmp/aa/bb /tmp/aa /tmp
[root@doumadou.github.io bb]# pushd cc
/tmp/aa/bb/cc
/tmp/aa/bb/cc /tmp/aa/bb /tmp/aa /tmp
[root@doumadou.github.io cc]# pushd dd
/tmp/aa/bb/cc/dd
/tmp/aa/bb/cc/dd /tmp/aa/bb/cc /tmp/aa/bb /tmp/aa /tmp
[root@doumadou.github.io dd]# pwd
/tmp/aa/bb/cc/dd
[root@doumadou.github.io dd]# popd
/tmp/aa/bb/cc /tmp/aa/bb /tmp/aa /tmp
[root@doumadou.github.io cc]# pwd
/tmp/aa/bb/cc
[root@doumadou.github.io cc]# popd
/tmp/aa/bb /tmp/aa /tmp
[root@doumadou.github.io bb]# popd
/tmp/aa /tmp
[root@doumadou.github.io aa]# popd
/tmp
[root@doumadou.github.io tmp]# 

```
## cd 自动更改错误的目录名(shopt -s cdspell)
```
[root@doumadou.github.io tmp]# ls  /var/
adm  cache  crash  db  empty  games  gopher  kerberos  lib  local  lock  log  mail  nis  opt  preserve  run  spool  tmp  var  yp
[root@doumadou.github.io tmp]# cd /var/game
bash: cd: /var/game: No such file or directory
[root@doumadou.github.io tmp]# shopt -s cdspell
[root@doumadou.github.io tmp]# cd /var/game
/var/games
[root@doumadou.github.io games]# pwd                                                 
/var/games
[root@doumadou.github.io games]# 
```

## ac 显示用户连接时间
```
# ac -p
```

## join

join的文件必须是已经排序的
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# cat test2.txt 
100 $5,000
200 $500
300 $3,000
400 $1,250
[root@doumadou.github.io tmp]# join test2.txt test1.txt 
100 $5,000 Jason Smith
200 $500 John Doe
300 $3,000 Sanjay Gupta
400 $1,250 Ashok Sharma
[root@doumadou.github.io tmp]# join test1.txt test2.txt 
100 Jason Smith $5,000
200 John Doe $500
300 Sanjay Gupta $3,000
400 Ashok Sharma $1,250
[root@doumadou.github.io tmp]# 
```

如果要将２个文件进行行与的合并，且没有排序字段，可以先用sed, awk等命令在文件前加入行号，然后再进行join.

## tr命令
将文件中的小写字母全部换成大小
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# tr a-z A-Z < test1.txt 
100 JASON SMITH
200 JOHN DOE
300 SANJAY GUPTA
400 ASHOK SHARMA
```

大小写互换
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# tr a-zA-Z A-Za-z < test1.txt 
100 jASON sMITH
200 jOHN dOE
300 sANJAY gUPTA
400 aSHOK sHARMA
```

sed 实现
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# sed 's/[a-z]/\U&/g' test1.txt 
100 JASON SMITH
200 JOHN DOE
300 SANJAY GUPTA
400 ASHOK SHARMA
[root@doumadou.github.io tmp]# sed 's/[a-z]/\u&/g' test1.txt 
100 JASON SMITH
200 JOHN DOE
300 SANJAY GUPTA
400 ASHOK SHARMA
```

## tune2fs 查看文件系统信息

## ssh免密码登陆远程主机
* 本机 使用ssh-key-gen安全公钥和私钥。 
* 本机 将公钥传给远程主机(ssh-copy-id)
```
# ssh-copy-id -i ~/.ssh/id_rsa.pub remote-host
```

## crontab
```
{minute} {hour} {day-of-month} {month} {day-of-week} {full-path-to-shell-script}
*/5 * * * * ifconfig 每5分钟执行
```

## *.bash_* 执行次序

/etc/profile; ~/.bash_profile; ~/.bash_rc; ~/.bash_login; ~/.profile; ~/.bash_logout;

* 交互式登陆执行次序
```
execute /etc/profile
IF ~/.bash_profile exists THEN
    execute ~/.bash_profile              ; ~/.bash_profile --> ~/.bash_rc --> /etc/bashrc
ELSE
    IF ~/.bash_login exist THEN
        execute ~/.bash_login
    ELSE
        IF ~/.profile exist THEN
            execute ~/.profile
        END IF
    END IF
END IF
```

* 登出 `~/.bash_logout`

* 非交互式登陆执行次序
```
~/.bashrc
```

## 产生随机数

```
# echo $RANDOM  (number between 0 – 32767)
```

## Shell脚本Debug

在脚本文件的顶部加入`set -xv` 或者执行脚本时，加`-xv` 参数。

## shell脚本中`'`与`"`的区别
```
[07:17:20][root@doumadou.github.io ~]# echo '$HOME'
$HOME
[07:17:20][root@doumadou.github.io ~]# echo "$HOME"
/root
```


## sar监控信息
```
# sar -u # CPU信息
# sar -u -p ALL
# sar -n DEV # 网络设备信息
# sar -d # 磁盘IO
```

## nice/renice

## cd命令补全大小写不敏感

```
[root@doumadou.github.io ~]# ls  
11.sql  TEST  mysql  test  tt
[07:17:20][root@doumadou.github.io ~]# bind "set completion-ignore-case on"
[07:17:20][root@doumadou.github.io ~]# cd t 
TEST/ test/ tt/   
```

## 多sesson ssh登陆远程主机使用单一网络链接

```
Host *
ControlMaster auto
ControlPath /tmp/ssh-%r@%h
```
```
    %r – remote login name
    %h – host name ( remote )
    %p – port
```
