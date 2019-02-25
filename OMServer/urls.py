"""OMServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url,re_path,include

from .views import index,test,test1,login_view,logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login_url'),
    path('logout/', logout_view, name='logout_url'),
    path('index/',index, name='home_url'),
    path('test/', test, name='test_url'),
    path('test1/', test1, name='test1_url'),
    re_path('^assets/',include('asset.urls')),
    re_path('^monitor/', include('monitor.urls')),
    re_path('^coderelease/', include('coderelease.urls')),
    re_path('^perecord/', include('perecord.urls')),
    re_path('^platman/', include('platmanagement.urls')),
    re_path('^cloud/', include('cloudmanagement.urls')),
]
