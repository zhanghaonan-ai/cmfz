import json
import random
import string
import time

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from cmfz_user.models import User
from redis import Redis
red = Redis(host='127.0.0.1', port=6379)
#获取单页的用户信息
def get_list(request):
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(User.objects.all().order_by('id'))
    paginator = Paginator(st_list, int(rows))
    try:
        rows = list(paginator.page(page).object_list)
    except:
        rows = list(paginator.page(int(page) - 1).object_list)
        page = int(page) - 1

    page_data = {
        'page': page,
        'total': paginator.num_pages,
        'records': paginator.count,
        'rows': rows
    }

    def mydefault(u):
        if isinstance(u, User):
            return {
                'id': u.id,
                'name': u.name,
                'religions_name': u.religions_name,
                'password': u.password,
                'salt': u.salt,
                'email': u.email,
                'status': u.status,
                'last_login_time': u.last_login_time.strftime("%Y-%m-%d %H:%M:%S"),
                'address': u.address,
            }

    data = json.dumps(page_data, default=mydefault)
    return HttpResponse(data)

#修改、删除
@csrf_exempt
def edit(request):
    oper = request.POST.get('oper')
    name = request.POST.get('name')
    id = request.POST.get('id')
    religions_name = request.POST.get('religions_name')
    password = request.POST.get('password')
    address = request.POST.get('address')
    status = True if request.POST.get('status') == 'true' else False
    email = request.POST.get('email')

    if oper == 'edit':
        user = User.objects.get(id=id)
        user.status = status
        user.name = name
        user.religions_name = religions_name
        user.password = password
        user.address = address
        user.email = email
        user.save()
    elif oper == 'del':
        User.objects.get(id=id).delete()
    return HttpResponse()

#添加
@csrf_exempt
def add(request):
    user_name = request.POST.get('user_name')
    religions_name = request.POST.get('religions_name')
    password = request.POST.get('password')
    email = request.POST.get('email')
    address = request.POST.get('address')
    status = True
    salt1 = ''.join(random.sample(string.digits, 6))
    print(user_name,religions_name,password,email,address,salt1)
    User.objects.create(name=user_name, religions_name=religions_name, password=password,
                        salt=salt1, status=status, address=address, email=email)
    return JsonResponse({'status': 1})


#检查用户名是否重复
def check_username(request):
    user_name = request.GET.get('user_name')
    name1=User.objects.values_list('name')
    print(user_name)
    if user_name in name1:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

#获取上半年的注册折线图
def get_half_year(request):
    if red.get('get_half_year'):
        data1 = red.get('get_half_year')
        data = eval(str(data1, encoding = "utf-8"))
        print(data, type(data))
    else:
        users = User.objects.all()
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count6 = 0
        for i in users:
            time = i.register_time
            list1 = str(time).split('-')
            print(list1[1])
            if list1[1] == '01':
                count1 += 1
            elif list1[1] == '02':
                count2 += 1
            elif list1[1] == '03':
                count3 += 1
            elif list1[1] == '04':
                count4 += 1
            elif list1[1] == '05':
                count5 += 1
            elif list1[1] == '06':
                count6 += 1

        x = ['1月', '2月', '3月', '4月', '5月', '6月']
        print(count1, count2, count3, count4, count5, count6)
        y = [count1, count2, count3, count4, count5, count6]
        data = {
            'x': x,
            'y': y,
        }
        red.set('get_half_year', str(data), ex = 60)
    return JsonResponse({'data': data})



#获取全国用户分布数据
def get_distribute(request):
    if red.get('get_distribute'):
        data1=red.get('get_distribute')
        data=eval(str(data1,encoding = "utf-8"))
        print(data,type(data))
    else:
        provinces = ["北京", "天津", "河北", "山西", "内蒙古", "吉林", "黑龙江", "辽宁", "上海", "江苏", "浙江", "安徽",
                     "福建", "江西", "山东", "河南", "湖北", "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏",
                     "陕西", "甘肃", "青海", "宁夏", "新疆", "香港", "澳门", "台湾"
                     ]
        data = []
        for i in provinces:
            data.append({'name': i, 'value': len(User.objects.filter(address=i))})
            red.set('get_distribute', str(data),ex = 60)

    return JsonResponse({'data': data})


def user_list(request):
    """渲染用户信息界面"""
    return render(request, 'user/user_list.html')


def user_register(request):
    """渲染用户注册趋势图界面"""
    return render(request, 'user/user_register.html')


def user_distributed(request):
    """渲染用户全国分布图界面"""
    return render(request, 'user/user_distributed.html')
