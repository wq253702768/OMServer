# Generated by Django 2.1.3 on 2018-12-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderelease', '0013_releasehost_data_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='addprojectrecode',
            name='release_status',
            field=models.CharField(choices=[('1', '未发布'), ('2', '发布中'), ('3', '发布完成'), ('4', '发布失败')], default='1', max_length=16, verbose_name='发布状态'),
        ),
    ]
