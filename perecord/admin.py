from django.contrib import admin

# Register your models here.
from .models import *


class OverTimeAdmin(admin.ModelAdmin):
    list_display = ["name", "s_time", "e_time", "overtime_hours", "memo", "c_time"]


admin.site.register(OverTime, OverTimeAdmin)