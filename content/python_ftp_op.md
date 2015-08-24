Title: python利用ftp批量上传下载文件
Category: python
Tags: python, ftplib
Date: 2015-08-14 00:10:28
---


批量上传本地的jpg图片到ftp服务器

~~~python
#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from ftplib import FTP

def ftpconnect():
    ftp_server = '192.168.0.101'

	ftp = FTP()
	ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
	ftp.connect(ftp_server, 2121) #连接
	ftp.login() #登录，如果匿名登录则用空串代替即可

	return ftp
	
def uploadfile(ftp, localpath, remotedir="DCIM/Camera"):

    filename= os.path.basename(localpath)
    remotepath = os.path.join(remotedir, filename)
	fp = open(localpath,'rb')
	ftp.storbinary('STOR '+ remotepath ,fp) #上传文件
	ftp.set_debuglevel(0)
	fp.close() #关闭文件


ftp = ftpconnect()

fp = os.popen("ls *.jpg")
lines = fp.readlines()
for line in lines:
    print line.strip()
    uploadfile(ftp, line.strip())
fp.close()

~~~

批量下载ftp服务器上某个文件夹下的jpg图片


~~~python
#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
from ftplib import FTP

def ftpconnect():
    ftp_server = '192.168.0.104'

	ftp=FTP()
	ftp.set_debuglevel(2) #打开调试级别2，显示详细信息
	ftp.connect(ftp_server, 2121) #连接
	ftp.login() #登录，如果匿名登录则用空串代替即可

	return ftp
	
def downloadfile(ftp, remotepath):
	localpath = os.path.basename(remotepath)
	fp = open(localpath,'wb') #以写模式在本地打开文件
	ftp.retrbinary('RETR ' + remotepath, fp.write) #接收服务器上文件并写入本地文件
	ftp.set_debuglevel(0) #关闭调试
    fp.close()

def _remove_empty(array):
    return [x for x in array if x !='']

class Download:
    def __init__(self, ftp, parent_abs):
        self._ftp = ftp
        self._parent_abs = parent_abs
        self._file_list = []

    def downloadfilebypath(self, path):
        filename = _remove_empty(path.split(' '))
    
        filename = ' '.join(filename[8:]) #这里是得到文件名，不同的ftp版本，可能结果不一样
        if filename.endswith('.jpg'):
            self._file_list.append(filename)

    def startdown(self):
        for fn in self._file_list:
            remotepath = os.path.join(self._parent_abs, fn)
            print "Downfile file:" + remotepath
            downloadfile(self._ftp, remotepath)


f = ftpconnect()
d = Download(f, "DCIM/Camera")
f.dir('DCIM/Camera/', d.downloadfilebypath)

d.startdown()

~~~


注意事项：

如果ftp.dir回调函数中直接下载图片的话，会出现ftplib.error_reply: 200 Binary type set的错误，原因是ftp下载文件时，会发送其它ftp命令，导致ftp命令序列出错。因此回调函数中，仅仅保存文件名。dir命令执行完成后，再下载图片。
