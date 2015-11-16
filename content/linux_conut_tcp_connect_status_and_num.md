Title: linux统計TCP的各种status的count
Category: linux
Tags: []
Date: 2015-10-12 15:20:39
---

# grep/sort/unqiu/sed

~~~
	# netstat -n |grep -E '^tcp'|awk '{print $NF}' |sort |uniq -c
~~~

# sed

~~~
	# netstat -n | awk '/^tcp/ {++s[$NF]} END {for (i in s) print s[i], i}'
~~~
