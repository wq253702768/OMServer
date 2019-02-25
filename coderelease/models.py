from django.db import models
from asset.models import NIC
# Create your models here.


class ReleaseEnv(models.Model):
    name = models.CharField('环境slug[英文字母,数字组成]',max_length=50,unique=True)
    memo = models.CharField('备注', max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '环境'
        verbose_name_plural = "环境"


class ReleaseConfig(models.Model):
    env = models.OneToOneField(ReleaseEnv, on_delete=models.CASCADE)
    jenkins_url = models.CharField('Jenkins地址', max_length=100)
    jenkins_username = models.CharField('Jenkins用户名', max_length=50)
    jenkins_password = models.CharField('Jenkins密码', max_length=100)
    jenkins_credentials_id = models.CharField('jenkins_credentials_id', max_length=200)
    branch_name = models.CharField('分支', max_length=100)
    docker_registry_address = models.CharField('镜像库地址', max_length=100)
    api_server_address = models.CharField('Apiserver地址', max_length=100)
    namespace = models.CharField('Namespace', max_length=50)
    redis_password = models.CharField('Redis密码', max_length=100)
    rabbitmq_password = models.CharField('Rabbitmq密码', max_length=100)

    class Meta:
        verbose_name = '环境配置'
        verbose_name_plural = '环境配置'


class ReleaseProjectType(models.Model):
    name = models.CharField('项目Tag(英文)',max_length=10)
    data_path = models.TextField('部署路径')
    memo = models.CharField('备注', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目类型'
        verbose_name_plural = '项目类型'


class ReleaseHost(models.Model):
    env = models.ForeignKey(ReleaseEnv, on_delete=models.CASCADE,verbose_name='环境名')
    sn = models.ForeignKey(NIC,on_delete=models.CASCADE,verbose_name='SN')
    ip = models.GenericIPAddressField('IP地址', blank=True, null=True)
    server_name = models.CharField('部署服务',max_length=50)
    port = models.IntegerField('SSH端口')
    pro_type = models.ForeignKey(ReleaseProjectType,on_delete=models.CASCADE, verbose_name='项目类型')
    kwargs = models.TextField('kwargs',default='{}')
    data_path = models.TextField('部署路径')

    class Meta:
        verbose_name = '环境主机'
        verbose_name_plural = '环境主机'


class AddProjectRecode(models.Model):
    STATUS_CHOICES = (
        (u'1', u'未发布'),
        (u'2', u'发布中'),
        (u'3', u'发布完成'),
        (u'4', u'发布失败'),
    )
    pro_name = models.CharField('项目名称',max_length=100)
    pro_type = models.ForeignKey(ReleaseProjectType,on_delete=models.CASCADE,verbose_name='项目类型')
    principal = models.CharField('负责人',max_length=50)
    env_name = models.ForeignKey(ReleaseEnv,on_delete=models.CASCADE,verbose_name='环境')
    domain = models.CharField('域名',max_length=100, null=True, blank=True)
    git_url = models.TextField('git地址')
    branch = models.CharField('分支', max_length=32)
    host_list = models.TextField('主机信息',default='[]')
    data_path = models.TextField('部署路径')
    kwargs = models.TextField('kwargs')
    jenkins_url = models.TextField('jenkins 地址',default='')
    jenkins_username = models.CharField('jenkins 用户', max_length=100,default='')
    jenkins_password = models.CharField('jenkins 密码',max_length=100,default='')
    jenkins_credentials_id = models.CharField('凭据',max_length=200,default='')
    docker_registry = models.CharField('镜像库', max_length=200,default='')
    api_server = models.CharField('API Server', max_length=200,default='')
    namespace = models.CharField('命名空间', max_length=100,default='')
    redis_pass = models.CharField('redis 密码',max_length=100,default='')
    rabbit_pass = models.CharField('rabbit 密码', max_length=100,default='')
    release_status = models.CharField(choices=STATUS_CHOICES, max_length=16,default='1', verbose_name='发布状态')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='创建日期')
    u_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    def __str__(self):
        return self.pro_name

    class Meta:
        verbose_name = '项目管理'
        verbose_name_plural = '项目管理'
