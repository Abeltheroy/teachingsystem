# Generated by Django 3.1.2 on 2023-03-15 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_course_headline'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='like_course',
            field=models.IntegerField(default=0, verbose_name='点赞数'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_like', models.CharField(default='', max_length=28, verbose_name='是否点赞')),
                ('c', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course', verbose_name='课程ID')),
                ('s', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.student', verbose_name='学生ID')),
            ],
        ),
    ]
