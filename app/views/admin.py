from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from app.models import *
from app.utils.BootStrap import *
from django import forms


def list(request):
    # 检查用户是否已经登录
    info = request.session.get("info")
    if not info:
        return redirect('')
    return render(request, 'admin/admin_list.html', {"form": Admin.objects.all()})


class AdminReset(BootStrapModelForm):
    confirm_pwd = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ["password", "confirm_pwd"]

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 校验
        flag = Admin.objects.filter(id=self.instance.pk, password=pwd).exists()
        if flag:
            raise ValidationError("密码不能和之前一致")
        return pwd

    def clean_confirm_pwd(self):
        confirm = self.cleaned_data.get("confirm_pwd")
        pwd = self.cleaned_data.get("password")
        if confirm != pwd:
            raise ValidationError("两次输入的密码不一致")
        return confirm


def reset(request, nid):
    row_object = Admin.objects.filter(id=nid).first()
    title = "重置管理员{}的密码".format(row_object.username)
    if request.method == 'GET':
        form = AdminReset()
        return render(request, 'change.html', {"form": form, "title": title})
    form = AdminReset(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {"form": form, "title": title})


def course_list(request):
    return HttpResponse(True)


def forum(request):
    c_set = set()
    cs = Comment.objects.all()
    for i in cs:
        c_set.add(i.c_id)
    res = Course.objects.none()
    print(c_set)
    for j in c_set:
        c = Course.objects.filter(id=j.id)
        res |= c
    return render(request, 'admin/forum.html', {"course": res})


def forum_detail(request, cid):
    comment = Comment.objects.filter(c_id=cid).all()
    dicts = {}
    for i in comment:
        dicts[Student.objects.filter(id=i.s_id.id).first().username] = i.comment
    return render(request, 'admin/forum_detail.html', {"comment": dicts, "cid": cid})


def forum_delete(request, cid, name):
    sid = Student.objects.filter(username=name).first()
    Comment.objects.filter(c_id=cid, s_id=sid).delete()
    return forum_detail(request, cid)
