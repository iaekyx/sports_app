
from django.db import models
from django.contrib.auth.models import User
 
MEDIA_ADDR = "http://124.221.15.178:8000/media/"

class Article(models.Model):    #定义文章模型类
    space = models.CharField(max_length=100,verbose_name='地点')   #verbose_name是
    content = models.TextField(verbose_name='文章内容')
    publish_time = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    distance = models.TextField(verbose_name='距离')
    speed = models.TextField(verbose_name='速度')
    used_time = models.TextField(verbose_name='用时')
    likes = models.TextField(verbose_name='喜欢')
    username = models.TextField(verbose_name='用户名')
    avatar = models.ImageField(upload_to='avatar', default='', verbose_name='头像')
    post_id = models.TextField(verbose_name='用户id')
    def get_avatar_url(self):
    #返回头像的url
        return str(self.avatar)
    class Meta:
        db_table = 'article_tb'     #定义表名
        verbose_name = '文章'       #后台显示
        verbose_name_plural = verbose_name    #后台显示的复数
 
 
 
 
class Comment(models.Model):    #定义评论模型
    article = models.ForeignKey(to=Article,on_delete=models.DO_NOTHING,verbose_name='评论文章')
    comment_content = models.TextField(verbose_name='评论内容')
    comment_author = models.ForeignKey(to=User,on_delete=models.DO_NOTHING,verbose_name='评论者')
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    pre_comment = models.ForeignKey('self',on_delete=models.DO_NOTHING,null=True,verbose_name='父评论id')  #父级评论，如果没有父级则为空NULL, "self"表示外键关联自己
    avatar = models.ImageField(upload_to='avatar', default='', verbose_name='头像')
    nickname = models.TextField(verbose_name='名称')
    def get_avatar_url(self):
    #返回头像的url
        return  str(self.avatar)
    class Meta:
        db_table = 'comment_tb'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.TextField(verbose_name='昵称')
    address = models.TextField(verbose_name='地址')
    height = models.TextField(verbose_name='身高')
    weight = models.TextField(verbose_name='体重')
    avatar = models.ImageField(upload_to='avatar', default='', verbose_name='头像')
    distance = models.IntegerField(verbose_name='总距离')
    step = models.IntegerField(verbose_name='总步数')
    calorie = models.IntegerField(verbose_name='总卡路里')
    def get_avatar_url(self):
    #返回头像的url
        return  str(self.avatar)
  
    class Meta:
        db_table = 'profile_tb'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


