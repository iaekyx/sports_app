from django.contrib import admin
from .models import Article,Comment,UserProfile,LikeNum
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(LikeNum)
