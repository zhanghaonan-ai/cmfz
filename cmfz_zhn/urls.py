"""cmfz_zhn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from cmfz_home import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', include('cmfz_home.urls')),
    path('carousel/', include('cmfz_carousel.urls')),
    path('user/', include('cmfz_user.urls')),
    path('article/', include('cmfz_article.urls')),
    path('album/', include('cmfz_album.urls')),
    path('postman/', include('cmfz_postman.urls')),
    path('',views.home),
]
