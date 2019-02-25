from django.contrib import admin
from .models import *
# Register your models here.


class PlatformManagementAdmin(admin.ModelAdmin):
    list_display = ['env', 'plat_name', 'plat_url']


admin.site.register(PlatformManagement,PlatformManagementAdmin)