from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from app.utils.BootStrap import *
from django.http import JsonResponse
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
def add_comment(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        comment_text = request.POST.get('comment')
        student_id = request.session["info"]["id"]
        print(course_id, comment_text, student_id)
        # create new comment object and save it to the database
        s = Student.objects.filter(id = student_id).first()
        c = Course.objects.filter(id = course_id).first()
        comment = Comment(c_id=c, s_id=s, comment=comment_text)
        comment.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

