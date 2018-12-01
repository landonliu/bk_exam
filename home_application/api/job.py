# -*- coding: utf-8 -*-
import base64
from blueking.component import shortcuts
from common.mymako import render_json
import time


def get_host_mdc(request):
    script_content = base64.b64encode('''
    #!/bin/bash

MEMORY=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
DISK=$(df -h | awk '$NF=="/"{printf "%s", $5}')
CPU=$(top -bn1 | grep load | awk '{printf "%.2f%%", $(NF-2)}')
DATE=$(date "+%Y-%m-%d %H:%M:%S")
echo -e "$DATE|$MEMORY|$DISK|$CPU"
    ''')

    business_id = request.GET.get("business_id", "")
    ip = request.GET.get("ip", "")

    business_id = int(business_id)

    client = shortcuts.get_client_by_request(request)
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
            return render_json({"result": True, "data": {"mem": data[1], "disk": data[2], "cpu": data[3].replace("\n", "")}})

    return render_json({"result": False, "message": "脚本执行超时"})
