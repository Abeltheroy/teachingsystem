from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from app.utils.BootStrap import *
from django import forms
def popular(request):
    course = Course.objects.all().order_by('-num_subscribers')[0:80]
    return render(request, 'course/course_list.html', {"course":course})