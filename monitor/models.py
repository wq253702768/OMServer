from django.db import models
from coderelease.models import ReleaseEnv

# Create your models here.


class PodStatus(models.Model):
    env = models.ForeignKey('coderelease.ReleaseEnv', on_delete=models.CASCADE)
    pod_up = models.TextField('UP')
    pod_down = models.TextField('DOWN')
    c_time = models.DateTimeField('时间', auto_now_add=True)

    class Meta:
        verbose_name = 'POD状态监控'
        verbose_name_plural = "POD状态监控"
