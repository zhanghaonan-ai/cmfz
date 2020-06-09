from django.urls import path

from cmfz_article import views

app_name = 'article'

urlpatterns = [
    path('get_list/', views.get_list, name='get_list'),
    path('pic_upload/', views.pic_upload, name='pic_upload'),
    path('get_all_pic/', views.get_all_pic, name='get_all_pic'),
    path('add/', views.add, name='add'),
    path('edit/', views.edit, name='edit'),
    path('article_del/', views.article_del, name='article_del'),
    path('article_list/', views.article_list, name = 'article_list'),
]
