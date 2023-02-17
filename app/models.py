from django.db import models


# Create your models here.
class Course(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=255)
    price = models.FloatField(verbose_name='价格')
    num_subscribers = models.IntegerField(verbose_name='订阅人数')
    num_comments = models.IntegerField(verbose_name='评论人数')
    category = models.CharField(verbose_name='类别', max_length=255)
    language = models.CharField(verbose_name='语言', max_length=32)


class Admin(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    authority = models.CharField(verbose_name='权限', default=1, max_length=3)


class Student(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    authority = models.CharField(verbose_name='权限', default=0, max_length=3)
    gender_choices = {
        (1, "男"),
        (2, "女")
    }
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choices)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    birthday = models.DateField(verbose_name='出生日期')


class Subscribe(models.Model):
    s_id = models.ForeignKey(to="Student", to_field="id", on_delete=models.CASCADE, verbose_name='学生ID')
    c_id = models.ForeignKey(to="Course", to_field="id", on_delete=models.CASCADE, verbose_name="课程ID")

class Comment(models.Model):
    s_id = models.ForeignKey(to="Student", to_field="id", on_delete=models.CASCADE, verbose_name='学生ID')
    c_id = models.ForeignKey(to="Course", to_field="id", on_delete=models.CASCADE, verbose_name="课程ID")
    comment = models.CharField(verbose_name="评论", max_length=128)
