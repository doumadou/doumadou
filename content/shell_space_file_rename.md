Title: Linux shell 批量重命名带空格的文件
Category: linux
Tags: []
Date: 2015-11-24 17:43:32
---

~~~bash
ls |while read  file;do mv "$file" `echo $file|sed "s/ /_/g"` -v;done
~~~
