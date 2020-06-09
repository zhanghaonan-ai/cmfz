import datetime
import json
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mutagen.mp3 import MP3
from cmfz_album.models import Album, Chapter

#获取单页列表数据
def get_list(request):
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    st_list = list(Album.objects.all().order_by('id'))
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
        if isinstance(u, Album):
            return {
                'id': u.id,
                'title': u.title,
                'author': u.author,
                'broadcast': u.broadcast,
                'chapter_count': len(list(Chapter.objects.filter(album_id = u.id))),
                'score': u.score,
                'publish_time': u.publish_time.strftime("%Y-%m-%d %H:%M:%S"),
                'img_src': str(u.img_src),
            }
    data = json.dumps(page_data, default = mydefault)
    print(data)
    return HttpResponse(data)

#修改及删除
@csrf_exempt
def edit(request):
    oper = request.POST.get('oper')
    title = request.POST.get('title')
    id = request.POST.get('id')
    author = request.POST.get('author')
    broadcast = request.POST.get('broadcast')
    try:
        if oper == 'edit':
            album = Album.objects.get(id = id)
            album.author = author
            album.title = title
            album.broadcast = broadcast
            album.save()
        elif oper == 'del':
            Album.objects.get(id = id).delete()
    except:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

#添加
@csrf_exempt
def add(request):
    try:
        title = request.POST.get('title')
        author = request.POST.get('author')
        img_src = request.FILES.get('img_src')
        broadcast = request.POST.get('broadcast')
        score = request.POST.get('score')
        album = Album.objects.create(title = title, author = author, broadcast = broadcast, img_src = img_src,score = score)
        album.chapter_count = len(list(Chapter.objects.filter(album_id = album.id)))
        album.save()
    except:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

#获取子列表单页的数据
def chapters_ofalbum(request):
    rows = request.GET.get('rows', 2)
    page = request.GET.get('page', 1)
    album_id = request.GET.get('albumId')
    st_list = list(Chapter.objects.filter(album_id = album_id).order_by('id'))
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
        if isinstance(u, Chapter):
            return {
                'id': u.id,
                'title': u.title,
                'size': str(round(u.size / 1024 / 1024, 2)) + 'MB',
                'time_long': str(datetime.timedelta(seconds = u.time_long)),
                'url': str(u.url)
            }
    data = json.dumps(page_data, default = mydefault)
    print(data)
    return HttpResponse(data)

#子列表添加
@csrf_exempt
def chapter_add(request):
    title = request.POST.get('title')
    url = request.FILES.get('url')
    album_id = request.POST.get('albumID')
    size = url.size
    time_long = MP3(url).info.length
    try:
        Chapter.objects.create(title = title, url = url, album_id = int(album_id), size = float(size),time_long = time_long)
        album = Album.objects.get(id = int(album_id))
        album.chapter_count += 1
        album.save()
    except:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})

#子列表修改删除
@csrf_exempt
def chapter_edit(request):
    oper = request.POST.get('oper')
    title = request.POST.get('title')
    url = request.FILES.get('url')
    try:
        if oper == 'del':
            id = request.POST.get('id')
            Chapter.objects.get(id = id).delete()
        else:
            id = request.POST.get('chapter_id')
            chapter = Chapter.objects.get(id = id)
            chapter.title = title
            chapter.url = url if url else chapter.url
            chapter.save()
    except:
        return JsonResponse({'status': 0})
    return JsonResponse({'status': 1})



def album_list(request):
    return render(request, 'album/album_list.html')