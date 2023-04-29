from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class M1(MiddlewareMixin):
    """中间件"""

    def process_request(self, request):
        if request.path_info == '/register/':
            return
        if request.path_info == '/':
            return
        info_dict = request.session.get("info")
        if info_dict:
            return
        return redirect('/')
