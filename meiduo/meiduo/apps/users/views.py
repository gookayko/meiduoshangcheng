from django.shortcuts import render
# 注意此处应该用models里面定义的users.User
# 而不是系统里面的User,所以应该导入下面的,而不是这个
# from django.contrib.auth.models import User
# Create your views here.
from users.models import User
from .serializers import CreateUserSerializer

# url(r'^usernames/(?P<username>\w{5,20})/coutn/$',views.UsernameCountView.as_view())
from rest_framework import serializers

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from rest_framework.views import APIView
from .serializers import CreateUserSerializer


# list==>[user,user,user...] 一个列表，里面是一个个字典返回查到的对象，不是个数
# retrieve==>pk==>user 根据pk主键查询，返回查到的对象，不是个数
# list retrieve==>return objects
# APIView
#
class UsernameCountView(APIView):
    """用户名数量"""
    def get(self,request,username):
        """获取指定用户名数量"""
        count = User.objects.filter(username=username).count()

        data = {
            'username':username,
            'count':count
        }

        return Response(data)
    

# url(r'^mobiles/(?P<mobile>))1[3-9]\d{9}/count/$',views.MobileCountView.as_view())
class MobileCountView(APIView):
    """手机号数量"""
    def get(self,request,mobile):
        """获取指定手机号数量"""
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile':mobile,
            'count':count
        }

        return Response(data)

# CreateAPIView 相当于GenericAPIView和CreateModelMixin在一起的简写
# CreateAPIView 已经封装了操作
class UserCreateView(CreateAPIView):
    """user register"""
    # 注册用户==》创建用户
    # queryset = 》当前进行创建操作 不需要查询
    serializer_class = CreateUserSerializer
