# Generated by Django 2.1.4 on 2019-01-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perecord', '0004_auto_20190102_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overtime',
            name='c_time',
            field=models.DateTimeField(auto_now=True, verbose_name='create time'),
        ),
    ]
