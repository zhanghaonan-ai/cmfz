import random
import re
import string
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from redis import Redis
from cmfz_home import send_msg
# from cmfz_home.models import Admin
from cmfz_permission.models import User
from cmfz_zhn import settings
from cmfz_carousel.models import Carousel
from utils.init_permission import init_permission
#主页渲染
def home(request):
    if request.session.get('adminname'):
        carousels = list(Carousel.objects.all())[:3]
        menu_list = request.session.get('menu_list')
        print(menu_list)
        return render(request, 'home.html',
                      {'adminname': request.session.get('adminname'), 'carousels': carousels, 'menus': menu_list})
    else:
        return redirect('index:login')


#登陆渲染
# def login(request):
#     return render(request, 'login.html')

def login(request):
    return render(request, 'login_form.html')

#检测手机号是否合法
@csrf_exempt
def check_user(request):
    # red = Redis(host='127.0.0.1', port=6379)
    # mobile = request.POST.get('mobile')
    # # Admin.objects.create(name = mobile)
    # print(mobile)
    # try:
    #     if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and Admin.objects.filter(name=mobile):
    #         if red.get(mobile + '_2'):
    #             return JsonResponse({'status': 0})
    #         else:
    #             code = ''.join(random.sample(string.digits, 6))  # 生成随机验证码
    #             code='123456'#测试
    #             red.set(mobile + '_1', code, 60)  # 60秒的有效期
    #             red.set(mobile + '_2', mobile, 60)  # 60秒内只能发送一次
    #             yunpian=send_msg.YunPian(settings.API_KEY)
    #             yunpian.send_message(mobile,code)
    #         return JsonResponse({'status': 1})
    #     else:
    #         return JsonResponse({'status': 0})
    # except:
    #     pass
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        request.session['adminname'] = username
        # print(username, password)
        user = User.objects.get(name = username,password = password)
        # 处理权限相关的业务
        if not user:
            return JsonResponse({'status': 0,"msg": "用户或密码错误"})
        init_permission(user, request)
        return JsonResponse({'status': 1})
    except:
        return JsonResponse({'status': 0,"msg": "用户或密码错误"})


# 验证码成功后登陆逻辑
def login_form(request):
    red = Redis(host='127.0.0.1', port=6379)
    mobile = request.GET.get('mobile')
    code = request.GET.get('code')
    # print(mobile,code)
    if re.match(r'^[1][3,4,5,7,8][0-9]{9}$', mobile) and User.objects.filter(name=mobile):
        redis_code = red.get(mobile + '_1').decode()
        # print(redis_code)
        if redis_code == code:
            request.session['adminname'] = mobile
            init_permission(User.objects.get(name = mobile), request)
            return JsonResponse({'status': 1})  # 验证码验证成功
        else:
            return JsonResponse({'status': 0})  # 验证码验证失败
    else:
        return JsonResponse({'status': 0})