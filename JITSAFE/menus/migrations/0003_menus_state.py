# Generated by Django 5.1.2 on 2024-12-20 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='state',
            field=models.IntegerField(null=True, verbose_name='状态'),
        ),
    ]
