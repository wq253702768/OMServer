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
from django.urls import path,re_path
from .views import *

urlpatterns = [
    path('project/list/',project_list, name='coderelease_project_list_url'),
    path('project/add/', project_add, name='coderelease_project_add_url'),
    path('ops/release/', project_release, name='ops_project_release_url'),
    path('ops/celery/', task_celery_reslut, name='ops_celery_task_url'),
    path('ops/test/', test, name='ops_project_test_url'),
    re_path('project/edit/(?P<pro_id>[0-9]+)', project_edit, name='coderelease_project_edit_url'),
    re_path('project/detail/(?P<pro_id>[0-9]+)', project_detail, name='coderelease_project_detail_url')

]
