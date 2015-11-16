#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Gavin'
SITENAME = u'LearnLog'
SITEURL = 'http://doumadou.github.io'

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('MarkDown语法', 'http://www.appinn.com/markdown/'),
		 ('在线MarkDown', 'http://mahua.jser.me/'),
		 ('Mysql开发手册', 'http://dev.mysql.com/doc/internals/en/index.html'),
		 ('Linux源码下载', 'https://www.kernel.org/pub/linux/kernel/'),
		 ('Epel软件包下载', 'http://dl.fedoraproject.org/pub/epel/'),
		 ('Linux软件包下载', 'ftp://195.220.108.108/linux/'),
		 ('RPM包搜索引擎', 'http://rpmfind.net/linux/rpm2html/search.php'),
		 ('AIX RPM包', 'http://www.oss4aix.org/download/RPMS'),
		 )

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

THEME = './theme/niu-x2-sidebar'

## 插件目录
PLUGIN_PATHS = [u"pelican-plugins"]

MD_EXTENSIONS = (['extra', 'codehilite', 'headerid'])
PLUGINS = ['extract_headings']

JINJA_EXTENSIONS = [
				    'jinja2.ext.ExprStmtExtension',
					]

NIUX2_DUOSHUO_SHORTNAME="doumadou"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
