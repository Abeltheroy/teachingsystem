from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import *
from app.utils.BootStrap import *
from django.http import JsonResponse
from django import forms
from django.urls import reverse
import random


def popular(request):
    course = Course.objects.all().order_by('-num_subscribers')[0:80]
    return render(request, 'course/course_list.html', {"course": course})


class SubscribeForm(BootStrapModelForm):
    class Meta:
        model = Subscribe
        fields = ["s_id", "c_id"]


def my_subscribe(request, nid):
    cid_list = Subscribe.objects.filter(s_id=nid).all().values_list("c_id", flat=
                                                                  True)
    c_list = []
    for i in cid_list:
        c_list.append(i)
    course = Course.objects.none()
    for i in c_list:
        c = Course.objects.filter(id=i)
        course |= c
    print(course)
    return render(request, 'course/subscribe_list.html', {"course": course})


@csrf_exempt
def subscribe(request):
    form = SubscribeForm(data=request.POST)
    form.save()
    return JsonResponse(True)


def cancel_subscribe(request):
    ins = Subscribe.objects.filter(c_id=request.GET.get("c_id"), s_id=request
                                   .GET.get("s_id")).first()
    if not ins:
        return JsonResponse({"status": False})
    ins.delete()
    return JsonResponse({"status": True})


class CommentForm(BootStrapModelForm):
    class Meta:
        model = Comment
        fields = ["comment", "s_id", "c_id"]


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


@csrf_exempt
def add_comment(request):
    form = CommentForm(data=request.POST)
    form.save()
    return JsonResponse({'success': True})


def like(request, nid):
    course = Course.objects.filter(id=nid).first()
    course.like_course = course.like_course + 1
    course.save()
    return detail(request, nid)
