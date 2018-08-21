---
layout: post
title: wordpress相关配置
category: wordpress 
tags: [wordpress]
date: 2018-08-21 09:30:35
---

# 隐藏后台登陆地址

使用代码

如果你不喜欢插件，可以将下面的代码添加到当前主题的 functions.php 文件：

```
//保护后台登录
add_action('login_enqueue_scripts','login_protection');  
function login_protection(){  
    if($_GET['word'] != 'press')header('Location: http://www.doc5188.com/');  
}
```
这样一来，后台登录的唯一地址就是 http://www.doc5188.com/wp-login.php?word=press，如果不是这个地址，就会自动跳转到 https://www.doc5188.com/ ，不信你试试！

你可以修改第 4 行的 Word、press 和 https://www.doc5188.com/ 这三个参数。

# 禁用wordpress cron。

修改wp-config.php

添加如下代码:
```
define('DISABLE_WP_CRON', true);
```
