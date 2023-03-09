# Generated by Django 3.1.2 on 2023-03-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='img_url',
            field=models.CharField(default='', max_length=40, verbose_name='图片地址'),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.SmallIntegerField(choices=[(2, '女'), (1, '男')], verbose_name='性别'),
        ),
    ]