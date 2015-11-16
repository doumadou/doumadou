Title: ubuntu终端自动修改ssh登陆后的标题
Category: linux
Tags: ssh
Date: 2015-11-16 15:42:17
---

自动修改ssh登陆后的标题主要通过修改openssh的源码实现

修改当前session的PS1环境变量。

~~~c/c++
openssh-5.9p1$ git diff .
diff --git a/clientloop.c b/clientloop.c
index 18a85c5..1c2079f 100644
--- a/clientloop.c
+++ b/clientloop.c
@@ -1468,6 +1468,7 @@ client_loop(int have_pty, int escape_char_arg, int ssh2_chan_id)
 
        /* Main loop of the client for the interactive session mode. */
        while (!quit_pending) {
+               fprintf(stderr, "%c]0;%s%c", '\033', host, '\007');
 
                /* Process buffered packets sent by the server. */
                client_process_buffered_input_packets();

~~~
