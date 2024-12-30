# Generated by Django 5.1.2 on 2024-12-20 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_enroll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True, verbose_name='角色名称')),
            ],
            options={
                'verbose_name': '角色',
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='UserRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='roles.roles', verbose_name='角色')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户角色关联',
                'db_table': 'user_roles',
            },
        ),
    ]