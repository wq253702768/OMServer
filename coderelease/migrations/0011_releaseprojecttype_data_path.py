# Generated by Django 2.1.3 on 2018-12-17 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderelease', '0010_auto_20181217_1034'),
    ]

    operations = [
        migrations.AddField(
            model_name='releaseprojecttype',
            name='data_path',
            field=models.TextField(default=datetime.datetime(2018, 12, 17, 20, 1, 25, 814), verbose_name='部署路径'),
            preserve_default=False,
        ),
    ]
