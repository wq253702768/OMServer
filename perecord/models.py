from django.db import models

# Create your models here.


class OverTime(models.Model):
    name = models.CharField(verbose_name='UserName', max_length=100)
    s_time = models.CharField(verbose_name='start time', max_length=100)
    e_time = models.CharField(verbose_name='end time',max_length=100)
    overtime_hours = models.CharField(verbose_name='working hours',max_length=20)
    c_time = models.DateTimeField(verbose_name='create time',auto_now=True)
    memo = models.TextField(null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    verbose_name = 'OverTime'
    verbose_name_plural = "OverTime"