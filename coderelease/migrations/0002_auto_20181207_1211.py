# Generated by Django 2.1.3 on 2018-12-07 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
        ('coderelease', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenkins_url', models.CharField(max_length=100, verbose_name='Jenkins地址')),
                ('jenkins_username', models.CharField(max_length=50, verbose_name='Jenkins用户名')),
                ('jenkins_password', models.CharField(max_length=100, verbose_name='Jenkins密码')),
                ('jenkins_credentials_id', models.CharField(max_length=200, verbose_name='jenkins_credentials_id')),
                ('branch_name', models.CharField(max_length=100, verbose_name='分支')),
                ('docker_registry_address', models.CharField(max_length=100, verbose_name='镜像库地址')),
                ('api_server_address', models.CharField(max_length=100, verbose_name='Apiserver地址')),
                ('namespace', models.CharField(max_length=50, verbose_name='Namespace')),
                ('redis_password', models.CharField(max_length=100, verbose_name='Redis密码')),
                ('rabbitmq_password', models.CharField(max_length=100, verbose_name='Rabbitmq密码')),
                ('env', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderelease.ReleaseEnv')),
            ],
            options={
                'verbose_name': '环境配置',
                'verbose_name_plural': '环境配置',
            },
        ),
        migrations.CreateModel(
            name='ReleaseHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('server_name', models.CharField(max_length=50, verbose_name='部署服务')),
                ('port', models.IntegerField(max_length=7, verbose_name='SSH端口')),
                ('env', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderelease.ReleaseEnv', verbose_name='环境名')),
            ],
            options={
                'verbose_name': '环境主机',
                'verbose_name_plural': '环境主机',
            },
        ),
        migrations.CreateModel(
            name='ReleaseProjectType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='项目Tag(英文)')),
                ('memo', models.CharField(max_length=100, verbose_name='备注')),
            ],
            options={
                'verbose_name': '项目类型',
                'verbose_name_plural': '项目类型',
            },
        ),
        migrations.AddField(
            model_name='releasehost',
            name='pro_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coderelease.ReleaseProjectType', verbose_name='项目类型'),
        ),
        migrations.AddField(
            model_name='releasehost',
            name='sn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asset.NIC', verbose_name='SN'),
        ),
    ]
