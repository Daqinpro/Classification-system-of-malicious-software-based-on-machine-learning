# Generated by Django 5.1.2 on 2024-12-19 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, null=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=30, null=True, verbose_name='密码')),
                ('state', models.IntegerField(null=True, verbose_name='状态')),
            ],
            options={
                'verbose_name': '用户',
                'db_table': 'user',
            },
        ),
    ]
