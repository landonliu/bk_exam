# -*- coding: utf-8 -*-
from django.db import models


class MonitorHost(models.Model):
    ip = models.CharField(max_length=20)
    biz_id = models.IntegerField()


class MonitorHostData(models.Model):
    ip = models.CharField(max_length=20)
    time = models.DateTimeField()
    # time = models.CharField(max_length=20)
    mem = models.CharField(max_length=10)
    disk = models.CharField(max_length=10)
    cpu = models.CharField(max_length=10)

