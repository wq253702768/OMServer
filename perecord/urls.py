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
    path('overtime/list/', overtime_list, name='perecord_overtime_list_url'),
    path('overtime/add/', overtime_add, name='perecord_overtime_add_url'),
    path('overtime/report/', report_overtime_list, name='report_overtime_list_url'),
    re_path('overtime/delete/(?P<overtime_id>[0-9]+)', overtime_delete, name='perecord_overtime_delete_url'),
    path('test/', test, name='perecord_test_url'),
]
