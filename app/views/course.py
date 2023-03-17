from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from app.utils.BootStrap import *
from django import forms
from django.urls import reverse
import random


def popular(request):
    course = Course.objects.all().order_by('-num_subscribers')[0:80]
    return render(request, 'course/course_list.html', {"course": course})


def my_subscribe(request, nid):
    course_id = Subscribe.objects.filter(s_id=nid)
    print(course_id)

    return render(request, 'course/subscribe_list.html')


def detail(request, nid):
    course = Course.objects.filter(id=nid).first()
    r = random.randint(2, 100)
    time = random.randint(40, 140)
    related_course = Course.objects.filter(category=course.category)[r:r + 3]
    comment = Comment.objects.filter(c_id=nid).all()
    dicts = {}
    for i in comment:
        # name_list.append(Student.objects.filter(id=i.s_id.id).first().username)
        dicts[Student.objects.filter(id=i.s_id.id).first().username] = i.comment
    return render(request, 'course/detail_list.html', {"course": course, "relate": related_course, "time": time,
                                                       "comment": dicts})


class CommentForm(BootStrapModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


def add_comment(request, nid):
    if request.method == 'GET':
        new = CommentForm()
        return render(request, "course/detail_list.html", {"new": new})
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('course.detail', args=[nid]))
