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
    path('report/', report, name='monitor_report_url'),
    path('env/status/',env_status_list, name='env_status_url'),
    re_path('env/status/detail/(?P<env_id>[0-9]+)', env_status_detail, name='env_status_detail_url')
]
