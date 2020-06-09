import re
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class CheckPermission(MiddlewareMixin):
    """对用户访问的请求进行限制"""

    def process_request(self, request):
        valid_url = [
            '/admin/.*',
            '/index/login/',
            '/index/check_user/',
            '/index/login_form/'
        ]
        current_url = request.path
        print('request.path', request.path)
        print('request.path_info', request.path_info)

        permission_list = request.session.get('permission_list')
        for url in valid_url:
            if re.match(url, current_url):
                return None

        if not permission_list:
            return redirect('index:login')

        if current_url in permission_list:
            return None

        return HttpResponse('无权访问！！！！')
