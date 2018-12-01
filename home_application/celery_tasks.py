# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
import time
from blueking.component import shortcuts
import base64
from home_application.models import MonitorHost, MonitorHostData


@task()
def async_task(x, y):
    """
    定义一个 celery 异步任务
    """
    logger.error(u"celery 定时任务执行成功，执行结果：{:0>2}:{:0>2}".format(x, y))
    return x + y


def execute_task():
    script_content = base64.b64encode('''
        #!/bin/bash

    MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
    DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
    CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    echo -e "$DATE|$MEMORY|$DISK|$CPU"
        ''')

    client = shortcuts.get_client_by_user("liubin")
    monitor_host_list = MonitorHost.objects.all()
    for monitor_host in monitor_host_list:
        business_id = monitor_host.biz_id
        ip = monitor_host.ip

        kwargs_fes = {
            "bk_biz_id": business_id,
            "script_content": script_content,
            "account": "root",
            "script_type": 1,
            "ip_list": [
                {
                    "bk_cloud_id": 0,
                    "ip": ip
                }
            ]
        }
        result_fes = client.job.fast_execute_script(**kwargs_fes)
        job_instance_id = result_fes["data"]["job_instance_id"]
        # 2018-12-01 10:34:06|9.99%|5%|0.00%
        kwargs_log = {
            "bk_biz_id": business_id,
            "job_instance_id": job_instance_id
        }

        for i in xrange(30):
            time.sleep(2)
            result_log = client.job.get_job_instance_log(**kwargs_log)
            if result_log["data"][0]["is_finished"]:
                log_content = result_log["data"][0]["step_results"][0]["ip_logs"][0]["log_content"]
                data = log_content.split("|")
                MonitorHostData.objects.create(ip=ip, time=data[0],
                                               mem=data[1].replace("%", ""), disk=data[2].replace("%", "")
                                               , cpu=data[3].replace("%", "").replace("\n", ""))
                return


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))
