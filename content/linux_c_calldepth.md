---
layout: post
title: linux c语言静态分析函数调用关系
category: linux
tags: [callgraph]
date: 2018-09-11 17:17:37
---

# 介绍Callgraph

Callgraph 实际由三个工具组合而成。

    一个是用于生成 C 函数调用树的 cflow 或者 calltree，下文主要介绍 cflow。
    一个处理 dot 文本图形语言的工具，由 graphviz 提升。建议初步了解下：DOT 语言。
    一个用于把 C 函数调用树转换为 dot 格式的脚本：tree2dotx

# 安装

```
    $ sudo apt-get install cflow graphviz gawk
    $ wget -c https://github.com/tinyclub/linux-0.11-lab/raw/master/tools/tree2dotx
    $ wget -c https://github.com/tinyclub/linux-0.11-lab/raw/master/tools/callgraph
    $ sudo cp tree2dotx callgraph /usr/local/bin
    $ sudo chmod +x /usr/local/bin/{tree2dotx,callgraph}
```

# 使用

```
   $ callgraph -f main -d ./main.c
```

# 原理分析

callgraph 实际上只是灵活组装了三个工具，一个是 cflow，一个是 tree2dotx，另外一个是 dot。

## cflow：拿到函数调用关系

```
    $ cflow -b -m main *.c > main.txt
```

## tree2dotx: 把函数调用树转换成 dot 格式

```
    $ cat main.txt | tree2dotx > main.dot
```

## 用 dot 工具生成可以渲染的图片格式

这里仅以 svg 格式为例：

```
    $ cat main.dot | dot -Tsvg -o main.svg
```
