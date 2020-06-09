import json
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from cmfz_carousel.models import Carousel

#获取轮播图信息
def get_list(request):
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(Carousel.objects.all().order_by('id'))
    paginator = Paginator(st_list, int(rows))
    try:
        rows = list(paginator.page(page).object_list)
    except :
        rows = list(paginator.page(int(page) - 1).object_list)
        page = int(page) - 1

    page_data = {
        'page': page,
        'total': paginator.num_pages,
        'records': paginator.count,
        'rows': rows
    }
    #转换格式
    def mydefault(u):
        if isinstance(u, Carousel):
            # print(u.status, u.img_url)
            return {
                'id': u.id,
                'desc': u.title,
                'date': u.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'status': u.status,
                'img_url': str(u.img_url),
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)

#修改 删除
@csrf_exempt
def edit(request):
    oper = request.POST.get('oper')
    desc = request.POST.get('desc')
    id = request.POST.get('id')
    status = request.POST.get('status')
    print(status)
    if oper == 'edit':
        car = Carousel.objects.get(id=id)
        if status == '1':
            car.status = True
        else:
            car.status = False
        car.title = desc
        car.save()
    elif oper == 'del':
        Carousel.objects.get(id=id).delete()
    return HttpResponse()

#添加
@csrf_exempt
def add(request):
    title = request.POST.get('title')
    if request.POST.get('status') == '1':
        status = True
    else:
        status=False
    print(status)
    pic = request.FILES.get('pic')
    Carousel.objects.create(title=title, status=status, img_url=pic)
    return HttpResponse()

#返回状态
def get_status(request):
    return HttpResponse("<select><option value='1'>显示</option>" + "<option value='0'>不显示</option></select>")




def carousel_list(request):
    return render(request, 'carousel/carousel_list.html')