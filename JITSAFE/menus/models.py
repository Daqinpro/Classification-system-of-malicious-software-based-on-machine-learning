from django.db import models
from rest_framework import serializers


class Menus(models.Model):
    name = models.CharField(max_length=20, verbose_name="菜单名称", null=True)
    path=models.CharField(max_length=100, verbose_name="菜单路径", null=True)
    icon=models.CharField(max_length=100, verbose_name="图标", null=True)
    state=models.IntegerField(verbose_name="状态",null=True)
    class Meta:
        db_table = 'menus'
        verbose_name = '菜单'
"""
序列化
"""
class MenusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = '__all__'
"""
菜单角色关联表
"""
class MenuRoles(models.Model):
    menu = models.ForeignKey("Menus", on_delete=models.CASCADE, verbose_name="菜单", null=True)
    role = models.ForeignKey("roles.Roles", on_delete=models.CASCADE, verbose_name="角色", null=True)

    class Meta:
        db_table = 'menu_roles'
        verbose_name = '菜单角色关联表'
