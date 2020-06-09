from django.urls import path
from cmfz_home import views
app_name='index'

urlpatterns = [
    path('home/',views.home,name="home"),#主页渲染
    path('login/', views.login, name='login'),#登录页渲染
    path('check_user/', views.check_user, name='check_user'),#验证手机号是否发送
    path('login_form/', views.login_form, name='login_form'),#验证成功后登录逻辑
]
