import numpy as np
from django.shortcuts import render, redirect, HttpResponse
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

from app.models import *


def recommend(request, sid):
    # 获取订阅数据，生成稀疏矩阵
    subs = Subscribe.objects.all().select_related('s_id', 'c_id')
    sub = Subscribe.objects.filter(s_id=sid).all()

    # 创建课程 ID 到整数的映射字典
    user_ids = [sub.s_id.id for sub in subs]
    course_ids = sorted(list(set(sub.c_id.id for sub in subs)))
    course_id_to_int = {course_id: i for i, course_id in enumerate(course_ids)}
    user_id_to_int = {user_id: i for i, user_id in enumerate(user_ids)}
    user_vectors = np.zeros((len(user_ids), len(course_ids)))
    for sub in subs:
        user_id = sub.s_id.id
        course_id = sub.c_id.id
        user_index = user_id_to_int[user_id]
        course_index = course_id_to_int[course_id]
        user_vectors[user_index, course_index] = 1

    # 获取与目标用户最相似的用户
    target_user_id = sid
    target_user_index = user_id_to_int[target_user_id]
    # 计算用户之间的相似度
    similarities = cosine_similarity(user_vectors)
    similar_users = similarities[target_user_index].argsort()[::-1][:5]

    # 将整数映射回课程 ID
    recommended_courses = set()
    for user_index in similar_users:
        user_id = user_ids[user_index]
        similar_subs = Subscribe.objects.filter(s_id=user_id).values_list('c_id', flat=True)
        similar_courses = Course.objects.filter(id__in=similar_subs)
        recommended_courses.update(similar_courses)
    print(recommended_courses)
    return render(request, 'course/recommend.html', {"course": recommended_courses})
