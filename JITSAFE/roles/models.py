from django.db import models

class Roles(models.Model):
    name = models.CharField(max_length=20, verbose_name="角色名称", null=True)
    class Meta:
        verbose_name = "角色"
        db_table="roles"
"""
用户角色关联表

"""
class UserRoles(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="用户", null=True)
    role = models.ForeignKey("Roles", on_delete=models.CASCADE, verbose_name="角色", null=True)
    class Meta:
        verbose_name = "用户角色关联"
        db_table="user_roles"
