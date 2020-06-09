import json
import os
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from cmfz_article.models import Pic, Article

#获取单页的文章信息信息
def get_list(request):
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(Article.objects.all().order_by('id'))
    paginator = Paginator(st_list, int(rows))
    try:
        rows = list(paginator.page(page).object_list)
    except Exception as tips:
        print(tips)
        rows = list(paginator.page(int(page) - 1).object_list)
        page = int(page) - 1

    page_data = {
        'page': page,
        'total': paginator.num_pages,
        'records': paginator.count,
        'rows': rows
    }

    def mydefault(u):
        if isinstance(u, Article):
            return {
                'id': u.id,
                'title': u.title,
                'publish_time': u.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'author': u.author,
                'cate': u.cate,
                'content': u.content
            }

    data = json.dumps(page_data, default=mydefault)
    print(data)
    return HttpResponse(data)

#添加
@csrf_exempt
def add(request):
    cate = True if request.POST.get('cate') == 'true' else False
    title = request.POST.get('title')
    content = request.POST.get('content')
    author = request.POST.get('author')
    print(cate, author, title, content)
    try:
        Article.objects.create(title=title, cate=cate, author=author, content=content)
    except Exception as tips:
        print(tips)
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

#修改
@csrf_exempt
def edit(request):
    id = request.POST.get('id')
    cate = True if request.POST.get('cate') == '显密法要' else False
    title = request.POST.get('title')
    content = request.POST.get('content')
    author = request.POST.get('author')
    print(cate, author, title, content)
    try:
        art = Article.objects.get(id=id)
        art.content = content
        art.author = author
        art.title = title
        art.cate = cate
        art.save()
    except:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

# 删除
@csrf_exempt
def article_del(request):
    oper = request.POST.get('oper')
    id = request.POST.get('id')
    if oper == 'del':
        Article.objects.get(id=id).delete()
    return HttpResponse()

#上传图片
@xframe_options_sameorigin  # 允许页面嵌套时发起访问
@csrf_exempt
def pic_upload(request):
    file = request.FILES.get("imgFile")
    if file:
        # 获取图片所在的服务的全路径
        img_url = request.scheme + "://" + request.get_host() + "/static/img/" + str(file)
        result = {"error": 0, "url": img_url}
        Pic.objects.create(img=file)
    else:
        result = {"error": 1, "url": "上传失败"}
    return HttpResponse(json.dumps(result), content_type="application/json")

#获取所有图片
def get_all_pic(request):
    # 找到图片所在的目录  方便进行回显
    pic_dir = request.scheme + "://" + request.get_host() + '/static/'
    pic_list = Pic.objects.all()
    rows = []
    for i in list(pic_list):
        # 获取图片的后缀
        path, pic_suffix = os.path.splitext(i.img.url)
        rows.append({
            "is_dir": False,
            "has_file": False,
            "filesize": i.img.size,
            "dir_path": "",
            "is_photo": True,
            "filetype": pic_suffix,
            "filename": i.img.name,
            "datetime": "2018-06-06 00:36:39"
        })

    data = {
        "moveup_dir_path": "",
        "current_dir_path": "",
        "current_url": pic_dir,
        "total_count": len(pic_list),
        "file_list": rows

    }
    return HttpResponse(json.dumps(data), content_type="application/json")



def article_list(request):
    return render(request, 'article/article_list.html')
