---
layout: post
title: AWK, SED, GREP
category: linux
tags: []
date: 2016-06-30 14:04:56
---

实例1: 给文件加入行号。

* sed
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# sed '=' test1.txt | sed 'N;s/\n/\t/'
1	100 Jason Smith
2	200 John Doe
3	300 Sanjay Gupta
4	400 Ashok Sharma

```

```
[root@doumadou.github.io tmp]# sed '=' test1.txt | sed 'N;s/\n/ /;s/^[0-9]\b/0&/'
01 100 Jason Smith
02 200 John Doe
03 300 Sanjay Gupta
04 400 Ashok Sharma
```

* awk 
```
[root@doumadou.github.io tmp]# cat test1.txt |awk '{print NR"\t"$0}'
1	100 Jason Smith
2	200 John Doe
3	300 Sanjay Gupta
4	400 Ashok Sharma

```

```
[root@doumadou.github.io tmp]# cat test1.txt |awk '{printf("%02d\t%s\n",NR,$0)}'
01	100 Jason Smith
02	200 John Doe
03	300 Sanjay Gupta
04	400 Ashok Sharma
```

VIM命令模式行前加入行号 `:%s/^/\=line('.')." "/g`

实例2: 将文件中的小写全部换成大写

* sed
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

* awk
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# awk '{print toupper($0)}' test1.txt 
100 JASON SMITH
200 JOHN DOE
300 SANJAY GUPTA
400 ASHOK SHARMA
```

实例3: 将文件中的大写全部换成小写

* sed
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]# sed 's/[A-Z]/\l&/g' test1.txt 
100 jason smith
200 john doe
300 sanjay gupta
400 ashok sharma
```

* awk 
```
[root@doumadou.github.io tmp]# cat test1.txt 
100 Jason Smith
200 John Doe
300 Sanjay Gupta
400 Ashok Sharma
[root@doumadou.github.io tmp]#  awk '{print tolower($0)}' test1.txt 
100 jason smith
200 john doe
300 sanjay gupta
400 ashok sharma
```

VIM全选，然后U, 将所有字符全部换成大写; u　全部换成小官

实例3: 获取文件指字行之间内容。
