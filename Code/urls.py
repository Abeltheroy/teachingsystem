"""Code URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.views import account, admin, course, stu, data, recommend

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', account.login),
    path('logout/', account.logout),
    path('information/<int:nid>/', stu.information),
    path('register/', stu.register),

    path('admin/list/', admin.list),
    path('admin/<int:nid>/reset/', admin.reset),

    path('stu/list/', stu.list),
    path('stu/add/', stu.add),
    path('stu/<int:nid>/modify/', stu.modify),
    path('stu/<int:nid>/delete/', stu.delete),

    path('course/list/', admin.course_list),
    path('comment/list/', admin.forum),
    path('forum/<int:cid>/', admin.forum_detail),
    path('forum/<int:cid>/<str:name>/delete/', admin.forum_delete),

    path('student/list/', stu.view),
    path('course/popular/', course.popular),
    path('course/subscribe/', course.subscribe),
    path('course/cancel_subscribe/', course.cancel_subscribe),
    path('course/<int:nid>/detail/', course.detail),
    path('course/add_comment/', course.add_comment),
    path('course/<int:nid>/like/', course.like),
    path('course/<int:nid>/my_subscribe/', course.my_subscribe),
    path('course/<int:sid>/recommend/', recommend.recommend),

    path('data/statistics/', data.statistics),
    path('data/bar/', data.bar),
    path('data/pie/', data.pie)

]
