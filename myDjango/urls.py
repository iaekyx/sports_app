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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.register),            #用户注册路由
    path('user_login/',views.user_login),        #用户登录路由
    path('index/',views.index),                  #首页路由
  #  re_path('article_detail/(\d)/',views.article_detail),  #文章详情页路由，并传入文章的id

    path('article_detail/',views.article_detail),  #文章详情页路由，并传入文章的id
    path('comment_control/',views.comment_control),   #提交评论处理的路由
    path('send_article/',views.send_article),
    path('send_sports_article/',views.send_sports_article),
    path('get_profile/',views.get_profile),
    path('get_image/',views.get_image),
    path('logout_view/',views.logout_view),
    path('get_information/',views.get_information),
    path('in_history/',views.in_history),
    path('get_history/',views.get_history),
    path('self_articles/',views.self_articles),
    path('add_likes/',views.add_likes),
    path('is_like/',views.is_like)
    ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
