# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=20)),
                ('biz_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MonitorHostData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=20)),
                ('time', models.CharField(max_length=20)),
                ('mem', models.CharField(max_length=10)),
                ('disk', models.CharField(max_length=10)),
                ('cpu', models.CharField(max_length=10)),
            ],
        ),
    ]
