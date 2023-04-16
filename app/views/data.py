from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from app.models import Course, Subscribe


def statistics(request):
    return render(request, 'data/statistics.list.html')


def bar(request):
    """ 构造柱状图 """
    legend = ['课程数量']

    x_axis = ['Business', 'Finance & Accounting', 'Lifestyle', 'Marketing', 'Development', 'Health & Fitness', 'Design',
              'Teaching & Academics'
        , 'IT & Software', 'Music', 'Photography & Video', 'Office Productivity', 'Office Productivity']
    sum = []
    for i in x_axis:
        sum.append(Course.objects.filter(category=i).count())
    series = [
        {
            "name": '课程数量',
            "type": 'bar',
            "data": sum
        }
    ]
    result = {
        "status": True,
        "data": {
            "legend": legend,
            "series_list": series,
            "x_axis": x_axis
        }
    }
    return JsonResponse(result)


def pie(request):
    s_id = request.GET.get("s_id")
    obj = Subscribe.objects.filter(s_id=s_id).all()
    cid_list = []
    for i in obj:
        cid_list.append(i.c_id)
    c_dict = {'Business': 0, 'Finance & Accounting': 0, 'Lifestyle': 0, 'Marketing': 0, 'Development': 0,
              'Health & Fitness': 0,
              'Design': 0, 'Teaching & Academics': 0, 'IT & Software': 0, 'Music': 0, 'Photography & Video': 0,
              'Office Productivity': 0}

    for i in cid_list:
        category = Course.objects.filter(id=i.id).first().category
        c_dict[category] += 1

    title = {
        "text": '已订阅',
        "left": 'center'
    }

    legend = {
        "orient": 'vertical',
        "left": 'left'
    }
    series = [
        {
            "name": 'Access From',
            "type": 'pie',
            "radius": '50%',
            "data": [
            ],
            "emphasis": {
                "itemStyle": {
                    "shadowBlur": 10,
                    "shadowOffsetX": 0,
                    "shadowColor": 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
    for key, value in c_dict.items():
        if value > 0:
            series[0]["data"].append({"value": value, "name": key})
    result = {
        "status": True,
        "series_data": series,
        "legend": legend,
        "title": title
    }
    return JsonResponse(result)
