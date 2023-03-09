from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from app.utils.BootStrap import BootStrapModelForm, BoorStrapForm
from django import forms


# Create your views here.
class LoginForm(BoorStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput
    )
    password = forms.CharField(label="密码", widget=forms.PasswordInput(render_value=True))


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 判断用户是否存在且判断是学生还是管理员
        admin_obj = Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            stu_obj = Student.objects.filter(**form.cleaned_data).first()
            if not stu_obj:
                form.add_error("password", "用户名或密码错误")
                return render(request, 'login.html', {"form": form})
            else:
                request.session["info"] = {'id': stu_obj.id, 'name': stu_obj.username}
                return redirect("/student/list")
        else:
            # 网站生产随机字符串，写入浏览器的cookie，再写入session
            request.session["info"] = {'id': admin_obj.id, 'name': admin_obj.username}
            return redirect("/admin/list")

    return render(request, 'login.html', {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/')
