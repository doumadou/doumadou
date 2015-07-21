Title: Django admin static文件404
Date: 2015-07-21 17:09
Category: Python
Tags: python, django
Slug: django_admin_css_404
Author: Gavin
Summary: Django admin 资源文件404


处理Django admin static的资源文件404的文件。

##方法一: 

  copy django下admin的static文件到项目中的static文件夹中。

##方法二:

  在urls.py中直接添加一条rule


	url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(django.__file__), "contrib/admin/static/admin/")})


   不要忘记在前面import os
  
