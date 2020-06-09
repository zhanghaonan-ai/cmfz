from django.urls import path

from cmfz_postman import views

app_name = 'postman'

urlpatterns = [
    path('first_page/', views.first_page, name = 'first_page'),
    path('album_detail/', views.album_detail, name = 'album_detail'),
    path('register/', views.register, name = 'rigster'),
    path('user_modify/', views.user_modify, name = 'user_modify'),
]
