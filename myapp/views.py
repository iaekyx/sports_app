from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth                #使用Django的auth认证组件
from django.contrib.auth.models import User    #使用Django的认证组件需要使用User用户表
from myapp.models import Article               #导入Article模型
from myapp.models import Comment               #导入Comment模型
import json
from django.core import serializers
 
def register(request):  #用户注册函数
   # username = request.POST.get('username')  #获取注册输入的信息
   # password = request.POST.get('password')
    json_data = request.body
    data = json.loads(json_data)
    username = data.get("username")
    password = data.get("password")
    User.objects.create_user(username=username,password=password)  #在User表创建用户记录
    return HttpResponse('注册成功')
 
 
def user_login(request):   #用户登录函数
    # username = request.POST.get('username')     #获取登录输入的信息

   # password = request.POST.get('password')
    json_data = request.body
    data = json.loads(json_data)
    username = data.get('username')
    password = data.get('password')
    user = auth.authenticate(username=username,password=password)  #用户验证
    if user:
        auth.login(request,user) #认证成功则保持登录状态
        data = {
            'code':200,
            "data":[{
                'id':user.id,
                'username':username,
                'password':password
                }]
        }
        # 将数据字典中的内容存储在一个名为 "res" 的字典中
        response_data = {"res": data}
        data_to_json = json.dumps(response_data)
        return HttpResponse(data_to_json,content_type='aplication/json')
    else:
        return HttpResponse('fail')  #认证失败则跳转到登录页面进行重新登录
 
 
def index(request):    #首页函数
    if request.user.username:      #判断用户是否已登录（用户名是否存在）
        all_article_list = Article.objects.all()    #取出所有的文章对象，结果返回一个QuerySet[]对象
      #  context = {
       #     'all_article_list': all_article_list
        #}
        data = serializers.serialize('json', all_article_list)

        return HttpResponse(data,content_type='application/json')
    else:
        return HttpResponse('error')   #如果用户没有登录，则跳转至登录页面
 
 
def article_detail(request,article_id):
    if request.user.username:
        article = Article.objects.get(id=article_id)    #从数据库找出id=article_id的文章对象
        comment_list = Comment.objects.filter(article_id=article_id)  #从数据库找出该文章的评论数据对象
        context = {
               'article': article,
               'comment_list': comment_list
        }
        return render(request,'article_detail.html',context=context)  #返回对应文章的详情页面
    else:
        return JsonResponse("error")
 
 
def comment_control(request):    #提交评论的处理函数
 
    if request.user.username:
        comment_content = request.POST.get('comment_content')
        article_id = request.POST.get('article_id')
        pid = request.POST.get('pid')
        author_id = request.user.id     #获取当前用户的ID
 
        Comment.objects.create(comment_content=comment_content,pre_comment_id=pid,article_id=article_id,comment_author_id=author_id)  #将提交的数据保存到数据库中
 
        article = list(Comment.objects.values('id','comment_content','pre_comment_id','article_id','comment_author_id','comment_time'))  #以键值对的形式取出评论对象，并且转化为列表list类型
 
        return JsonResponse(article,safe=False)   #JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False
    else:
        return HttpResponse("error")

def send_article(request):
    if request.user.username:
        title = request.POST.get('title')
        content = request.POST.get('content')
        auther_name = request.user.username
        article_id = request.user.id
        Article.objects.create(title=title,content=content,author=request.user)

        user_data = {
            'title':title,
            'content':content,
            'auther_name':auther_name,
        }
        user_data_as_json = json.dumps(user_data)
        return HttpResponse(user_data_as_json,content_type='application/json')

    else:
        HttpResponse("error")
    
