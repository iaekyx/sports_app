"""myDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,re_path
from myapp import views       #导入myapp中的视图函数
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register),            #用户注册路由
    path('user_login/',views.user_login),        #用户登录路由
    path('index/',views.index),                  #首页路由
    re_path('article_detail/(\d)/',views.article_detail),  #文章详情页路由，并传入文章的id
    path('comment_control/',views.comment_control),   #提交评论处理的路由
    path('send_article/',views.send_article)
]
