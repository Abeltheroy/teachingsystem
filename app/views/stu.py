from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe

from app.models import *
from app.utils.BootStrap import *
import random


class StuModelForm(BootStrapModelForm):
    class Meta:
        model = Student
        fields = ["username", "password", "age", "gender", "email", "birthday"]


def information(request, nid):
    row_object = Student.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = StuModelForm(instance=row_object)
        return render(request, 'stu/information.html', {"form": form, "title": "个人信息"})
    form = StuModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/student/list/')
    return render(request, 'stu/information.html', {"form": form})


def list(request):
    # 搜索
    data_dict = {}
    value = request.GET.get('q', "")
    if value:
        data_dict["username__contains"] = value

    # 分页
    page = int(request.GET.get("page", 1))
    page_size = 10
    start = (page - 1) * page_size
    end = page * page_size

    # 页码
    total_count = Student.objects.all().count()
    total, flag = divmod(total_count, page_size)
    if flag:
        total += 1
    page_str_list = []

    # 首页
    start_page = '<li><a href="/stu/list/?page={}">首页</a></li>'.format(1)
    page_str_list.append(start_page)
    # 上一页
    if page > 1:
        pre_page = '<li><a href="/stu/list/?page={}">上一页</a></li>'.format(page - 1)
    else:
        pre_page = '<li><a href="/stu/list/?page={}">上一页</a></li>'.format(1)
    page_str_list.append(pre_page)

    for i in range(1, total + 1):
        if i == page:
            ele = '<li class="active"><a href="/stu/list/?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="/stu/list/?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    # 下一页
    if page == total:
        next_page = '<li><a href="/stu/list/?page={}">下一页</a></li>'.format(total)
    else:
        next_page = '<li><a href="/stu/list/?page={}">下一页</a></li>'.format(page + 1)
    page_str_list.append(next_page)
    # 尾页
    end_page = '<li><a href="/stu/list/?page={}">尾页</a></li>'.format(total)
    page_str_list.append(end_page)
    page_string = mark_safe("".join(page_str_list))
    return render(request, 'stu/stu_list.html',
                  {"n1": Student.objects.filter(**data_dict)[start:end], "n2": value,
                   "page_string": page_string})


def add(request):
    if request.method == 'GET':
        form = StuModelForm()
        return render(request, 'add.html', {"form": form, "title": "新建用户"})
    form = StuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/stu/list')
    return render(request, 'add.html', {"form": form, "title": "新建用户"})


def modify(request, nid):
    row_object = Student.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = StuModelForm(instance=row_object)
        return render(request, 'add.html', {"form": form, "title": "编辑用户"})
    form = StuModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/stu/list/')
    return render(request, 'add.html', {"form": form, "title": "编辑用户"})


def delete(request, nid):
    Student.objects.filter(id=nid).delete()
    return redirect('/stu/list/')


def view(request):
    page = random.randint(1, 5025)
    page_size = 40
    start = page_size * (page - 1)
    end = page_size * page
    course = Course.objects.filter()[start:end]
    return render(request, 'stu/student_list.html', {"course": course})
