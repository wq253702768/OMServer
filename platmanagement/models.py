from django.db import models

# Create your models here.
from coderelease.models import ReleaseEnv


class PlatformManagement(models.Model):
    env = models.ForeignKey(ReleaseEnv, on_delete=models.CASCADE,verbose_name='环境名')
    plat_name = models.CharField(max_length=200,verbose_name='Platfrom name')
    plat_url = models.TextField(verbose_name='url')

    class Meta:
        verbose_name = 'Platform management'
        verbose_name_plural = 'Platform management'
