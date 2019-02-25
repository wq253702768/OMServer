from django.contrib import admin
from monitor import models
from coderelease.models import ReleaseEnv
# Register your models here.


class MonitorPodStatusAdmin(admin.ModelAdmin):

    list_display = ['pod_up', 'pod_down', 'c_time']


admin.site.register(models.PodStatus, MonitorPodStatusAdmin)