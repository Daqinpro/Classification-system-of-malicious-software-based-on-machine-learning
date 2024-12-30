from django.db import models
from rest_framework import serializers


class UserFiles(models.Model):
    name=models.CharField(max_length=100,verbose_name="备注",null=True)
    path=models.CharField(max_length=100,verbose_name="文件路径",null=True)
    url=models.CharField(max_length=100,verbose_name="访问路径",null=True)
    user=models.ForeignKey("users.User",on_delete=models.CASCADE,verbose_name="用户",null=True)
"""
序列化
"""
class UserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserFiles
        fields=("name","url","id")
class UserModel(models.Model):
    user=models.ForeignKey("users.User",on_delete=models.CASCADE,verbose_name="用户",null=True)
    UserFile=models.ForeignKey("UserFiles",on_delete=models.CASCADE,verbose_name="文件",null=True)
    Ramnit=models.IntegerField(verbose_name="Ramnit",null=True)
    Lollipop2=models.IntegerField(verbose_name="Lollipop2",null=True)
    Kelihos_ver3=models.IntegerField(verbose_name="Kelihos_ver3",null=True)
    Vundo=models.IntegerField(verbose_name="Vundo",null=True)
    Simda=models.IntegerField(verbose_name="Simda",null=True)
    Tracur=models.IntegerField(verbose_name="Tracur",null=True)
    Kelihos_ver1=models.IntegerField(verbose_name="Kelihos_ver1",null=True)
    Obfuscator_ACY=models.IntegerField(verbose_name="Obfuscator_ACY",null=True)
    Gatak=models.IntegerField(verbose_name="Gatak",null=True)
    class Meta:
        db_table="UserModel"
        verbose_name="用户模型"
"""
序列化
"""
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModel
        #排除id
        exclude = ['id','user','UserFile']
"""
用户模型数据id
"""
class UserModelDataId(models.Model):
    usermodel=models.ForeignKey("UserModel",on_delete=models.CASCADE,verbose_name="用户模型",null=True)
    file_id=models.CharField(max_length=100,verbose_name="id",null=True)
    class Meta:
        db_table="UserModelDataId"
        verbose_name="用户模型数据id"
class UserModelDataIdSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModelDataId
        fields="__all__"
class UserModelResult(models.Model):
    usermodeldataid=models.ForeignKey("UserModelDataId",on_delete=models.CASCADE,verbose_name="用户模型数据id",null=True)
    Ramnit=models.IntegerField(verbose_name="Ramnit",null=True)
    Lollipop2 = models.IntegerField(verbose_name="Lollipop2", null=True)
    Kelihos_ver3=models.IntegerField(verbose_name="Kelihos_ver3",null=True)
    Vundo=models.IntegerField(verbose_name="Vundo",null=True)
    Simda=models.IntegerField(verbose_name="Simda",null=True)
    Tracur=models.IntegerField(verbose_name="Tracur",null=True)
    Kelihos_ver1=models.IntegerField(verbose_name="Kelihos_ver1",null=True)
    Obfuscator_ACY=models.IntegerField(verbose_name="Obfuscator_ACY",null=True)
    Gatak=models.IntegerField(verbose_name="Gatak",null=True)
    class Meta:
        db_table="UserModelResult"
        verbose_name="用户模型数据结果"
class UserModelResultSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserModelResult
        fields="__all__"