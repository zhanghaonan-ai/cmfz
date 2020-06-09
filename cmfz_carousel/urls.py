from django.urls import path
from cmfz_carousel import views

app_name = 'carousel'

urlpatterns = [
    path('get_list/', views.get_list, name='get_list'),#获取单页信息
    path('edit/', views.edit, name='edit'),#修改 删除
    path('add/', views.add, name='add'),#添加
    path('get_status/', views.get_status, name='get_status'),#获取状态
    path('carousel_list/', views.carousel_list, name = 'carousel_list'),
]
