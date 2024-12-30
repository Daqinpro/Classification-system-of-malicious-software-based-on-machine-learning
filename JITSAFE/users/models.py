from django.db import models
from rest_framework import serializers


class User(models.Model):
    username = models.CharField(max_length=300,verbose_name="用户名",null=True)
    password = models.CharField(max_length=300,verbose_name="密码",null=True)
    state=models.IntegerField(verbose_name="状态",null=True)
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
"""
序列化
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','id','state')
"""
注册
"""
class Enroll(models.Model):
    email = models.EmailField(verbose_name="邮箱",null=True)
    code = models.CharField(max_length=6,verbose_name="验证码",null=True)
    class Meta:
        db_table = 'enroll'
        verbose_name = '注册'

