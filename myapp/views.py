from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth                #使用Django的auth认证组件
from django.contrib.auth.models import User    #使用Django的认证组件需要使用User用户表
from myapp.models import Article               #导入Article模型
from myapp.models import Comment               #导入Comment模型
from myapp.models import UserProfile
import json
from django.core import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
def register(request):  #用户注册函数
   # username = request.POST.get('username')  #获取注册输入的信息
   # password = request.POST.get('password')
    json_data = request.body
    data = json.loads(json_data)
    username = data.get("username")
    password = data.get("password")
    User.objects.create_user(username=username,password=password)  #在User表创建用户记录
    user = User.objects.filter(username=username).first()
    UserProfile.objects.create(user=user)

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
        old_token = Token.objects.filter(user=user)
        old_token.delete()
        # 创建新的Token
        token = Token.objects.create(user=user)
        data = {
            'code':200,
            "data":{
                'id':user.id,
                'username':username,
                'password':password,
                'token': token.key
                }
        }
        # 将数据字典中的内容存储在一个名为 "res" 的字典中
        response_data = {"res": data}
        data_to_json = json.dumps(response_data)
        return HttpResponse(data_to_json,content_type='aplication/json')
    else:
        return HttpResponse('fail')  #认证失败则跳转到登录页面进行重新登录
 
 
def index(request):    #首页函数
        all_article_list = Article.objects.all()
        #.values('id', "space","content","publish_time","author","distance","speed","used_time","likes","username","avatar")
      #  context = {
       #     'all_article_list': all_article_list
        #}

        # 使用 serializers.serialize 将查询集序列化为 JSON
        json_data = serializers.serialize('json', all_article_list)
        data1 = json.loads(json_data)
        all_article_list = [entry['fields'] for entry in data1]
       #response_data = {"res": article_list}
        data = {
                "data":all_article_list
        }
        response_data ={"res":data}
        result_json = json.dumps(response_data)
        return HttpResponse(result_json,content_type='application/json')
 
 
def article_detail(request,article_id):
        article = Article.objects.get(id=article_id)    #从数据库找出id=article_id的文章对象
        comment_list = Comment.objects.filter(article_id=article_id)  #从数据库找出该文章的评论数据对象
        all_article_list = [article]
        json_data = serializers.serialize('json', all_article_list)
        data1 = json.loads(json_data)
        article_list = [entry['fields'] for entry in data1]
        json_data = serializers.serialize('json', comment_list)
        data1 = json.loads(json_data)
        comment_list = [entry['fields'] for entry in data1]
       
        context = {
               'article': article_list,
               'comment_list': comment_list,
        }
        response_data ={"res":context}
        result_json = json.dumps(response_data)
        return HttpResponse(result_json,content_type='application/json')
  
         #return render(request,'article_detail.html',context=context)  #返回对应文章的详情页面
 
 
def comment_control(request):    #提交评论的处理函数
 
   # if request.user.username:
   #     comment_content = request.POST.get('comment_content')
   #     article_id = request.POST.get('article_id')
   #     pid = request.POST.get('pid')
        json_data = request.body
        data = json.loads(json_data)
        comment_content = data.get('comment_content')
        article_id = data.get('article_id')
        pid = data.get('pid')
        ID = data.get('id')
        user = User.objects.get(id=ID)
        author_id = user.id     #获取当前用户的ID
        profile = UserProfile.objects.get(user=user)
        Comment.objects.create(comment_content=comment_content,pre_comment_id=pid,article_id=article_id,comment_author_id=author_id,avatar=profile.get_avatar_url(),nickname=profile.nickname)  #将提交的数据保存到数据库中
 
        article = list(Comment.objects.values('id','comment_content','pre_comment_id','article_id','comment_author_id','comment_time'))  #以键值对的形式取出评论对象，并且转化为列表list类型
        article_to_json = JsonResponse(article,safe=False)
        return HttpResponse(article_to_json,content_type='aplication/json')
        #return JsonResponse(article,safe=False)   #JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False
   # else:
    #    return HttpResponse("error")

def send_article(request):
   # token_key = request.auth.key
   # token = Token.objects.get(key=token_key)
   # user = token.user
    #if request.user.username:
        #title = request.POST.get('title')
        #content = request.POST.get('content')
        json_data = request.body
        data = json.loads(json_data)
        space = data.get('space')
        content = data.get('content')
        ID = data.get('id')
        user = User.objects.get(id=ID)
        auther_name = user.username
        article_id = user.id
        likes = 0
        profile = UserProfile.objects.get(user=user)
        new_article=Article.objects.create(space=space,content=content,author=user,likes=likes,username=auther_name,avatar=profile.get_avatar_url())
        new_article.post_id=new_article.id
        new_article.save()
      
        user_data = {
            'space':space,
            'content':content,
            'auther_name':auther_name,
            'article_id':article_id,
            'likes':likes,
            'avatar':profile.get_avatar_url(),
            'post_id':new_article.post_id,
        }
        user_data_as_json = json.dumps(user_data)
        return HttpResponse(user_data_as_json,content_type='application/json')
    #else:
     #   return HttpResponse("error")
def send_sports_article(request):
    #if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        space = data.get('space')
        content = data.get('content')
        distance = data.get('distance')
        speed = data.get('speed')
        used_time = data.get('used_time')
        likes = 0
        ID = data.get('id')
        user = User.objects.get(id=ID)
        profile = UserProfile.objects.get(user=user)
       
       # title = request.POST.get('title')
       # content = request.POST.get('content')
        auther_name = user.username
        article_id = user.id
        new_article=Article.objects.create(space=space,content=content,distance=distance,speed=speed,used_time=used_time,author=user,likes=likes,username=auther_name,avatar=profile.get_avatar_url())
        new_article.post_id=new_article.id
        new_article.save()
        user_data = {
            'space':space,
            'content':content,
            'distance':distance,
            'speed':speed,
            'used_time':used_time,
            'article_id':article_id,
            'likes':likes,
            'post_id':new_article.post_id,
            'avatar':profile.get_avatar_url(),
        }
        user_data_as_json = json.dumps(user_data)
        return HttpResponse(user_data_as_json,content_type='application/json')

    #else:
     #   HttpResponse("error")

def get_profile(request):
   # if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        nickname = data.get('nickname')
        address = data.get('address')
        weight = data.get('weight')
        height = data.get('height')
        ID = data.get('id')
        user = User.objects.get(id=ID)
        profile = UserProfile.objects.get(user=user)
        profile.nickname=nickname
        profile.address=address
        profile.weight=weight
        profile.height=height
        profile.save()
        user_data = {
            'nickname':nickname,
            'address':address,
            'weight':weight,
            'height':height,
        }
        user_data_as_json = json.dumps(user_data)
        return HttpResponse(user_data_as_json,content_type='application/json')
   # else:
    #    return HttpResponse("error")

def get_image(request,ID):
#    if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        ID = data.get('id')
        user = User.objects.get(id=ID)
        profile = UserProfile.objects.get(user=user)

   # '''上传头像'''
 #   try:
        appLogger.debug('进入上传头像的接口')
        appLogger.debug('收到的请求={}'.format(request))
        appLogger.debug('收到的文件是={}'.format(request.FILES))
        avatar = request.FILES.getlist('file')[0]  # 获取头像名称
        appLogger.debug('收到的头像是={}'.format(avatar))
        profile.avatar.delete()
        profile.avatar = avatar
        profile.save()

        # 3. 拼接图片的路径
        avatar_addr = profile.get_avatar_url()
        appLogger.debug('返回的图片链接是={}'.format(avatar_addr))

        return successResultJson(data={"avatar": avatar_addr}, msg='修改成功')
 #   except Exception as e:
        # 打印异常,并且返回异常数据给前端
  #      return exception_fail_rasie(e=e, request=request)

def get_information(request):
  #  if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        ID = data.get('id')
        user = User.objects.get(id=ID)
        profile = UserProfile.objects.get(user=user)
        nickname=profile.nickname
        address=profile.address
        weight=profile.weight
        height=profile.height
        avatar=profile.avatar
        data = {
                'nickname':nickname,
                'address':address,
                'weight':weight,
                'height':height,
                'avatar':profile.get_avatar_url(),
        }
        response_data ={"res":data}
        result_json = json.dumps(response_data)
        return HttpResponse(result_json,content_type='application/json')

def in_history(request):
   # if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        distance = data.get('distance')
        step = data.get('step')
        calorie = data.get('calorie')
        ID = data.get('id')
        user = User.objects.get(id=ID)
        article_id = user.id
        profile = UserProfile.objects.get(user=user)
        profile.distance = profile.distance+distance
        profile.step = profile.step +step
        profiel.calorie = profile.calorie +calorie
        profile.save()
        user_data = {
            'distance':distance,
            'step': step,
            'calorie':calorie,
        }
        user_data_as_json = json.dumps(user_data)
        return HttpResponse(user_data_as_json,content_type='application/json')
  #  else:
  #      HttpResponse("error")

def get_history(request):
    # if request.user.username:
        json_data = request.body
        data = json.loads(json_data)
        ID = data.get('id')
        user = User.objects.get(id=ID)
        profile = UserProfile.objects.get(user=user)
        data={
                'distance':profile.distance,
                'step':profile.step,
                'calorie':profile.calorie,
        }
        response_data ={"res":data}
        result_json = json.dumps(response_data)
        return HttpResponse(result_json,content_type='application/json')

def self_articles(request):
        json_data = request.body
        data = json.loads(json_data)
        ID = data.get('id')
        user = User.objects.get(id=ID)
      
        article_list = Article.objects.filter(post_id=ID)    #从数据库找出id=article_id的文章对象
        json_data = serializers.serialize('json', article_list)
        data1 = json.loads(json_data)
        article_list = [entry['fields'] for entry in data1]
     
        context = {
               'article': article_list,
        }
        response_data ={"res":context}
        result_json = json.dumps(response_data)
        return HttpResponse(result_json,content_type='application/json')
  
def logout_view(request):
    logout(request)
    return HttpResponse("succeee")
