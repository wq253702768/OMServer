from django.contrib import admin

# Register your models here.
from coderelease import models


class ReleaseEnvAdmin(admin.ModelAdmin):
    list_display = ['name', 'memo']


class ReleaseConfigAdmin(admin.ModelAdmin):
    list_display = ['env', 'jenkins_url', 'jenkins_username', 'jenkins_password', 'jenkins_credentials_id', 'branch_name', 'docker_registry_address', 'api_server_address', 'namespace', 'redis_password', 'rabbitmq_password']


class ReleaseProjectTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'memo']


class ReleaseHostAdmin(admin.ModelAdmin):
    list_display = ['ip','sn','port','server_name','pro_type','env','data_path']


class AddProjectRecodeAdmin(admin.ModelAdmin):
    list_display = ['pro_name', 'pro_type', 'git_url', 'branch', 'host_list','env_name', 'principal', 'c_time', 'u_time']


admin.site.register(models.ReleaseEnv, ReleaseEnvAdmin)
admin.site.register(models.ReleaseConfig, ReleaseConfigAdmin)
admin.site.register(models.ReleaseProjectType, ReleaseProjectTypeAdmin)
admin.site.register(models.ReleaseHost, ReleaseHostAdmin)
admin.site.register(models.AddProjectRecode, AddProjectRecodeAdmin)