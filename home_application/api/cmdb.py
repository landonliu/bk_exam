# -*- coding: utf-8 -*-
from common.mymako import render_json
from blueking.component import shortcuts
from home_application.models import MonitorHost
import json


def search_business(request):
    client = shortcuts.get_client_by_request(request)
    kwargs = {
    }
    result = client.cc.search_business(**kwargs)
    return render_json(result)


def search_host(request):
    business_id = request.GET.get("business_id", "")
    body_data = request.body

    if not business_id:
        return render_json({"result": False, "message": "必须选择业务！"})

    ip_list_filter = body_data.split("\n")

    client = shortcuts.get_client_by_request(request)
    kwargs = {
        "ip": {
            "data": ip_list_filter,
            "exact": 0,
            "flag": "bk_host_innerip|bk_host_outerip"
        },
        "condition": [{
            "bk_obj_id": "biz",
            "fields": [],
            "condition": [
                {
                    "field": "bk_biz_id",
                    "operator": "$eq",
                    "value": int(business_id)
                }
            ]
        }]
    }
    result = client.cc.search_host(**kwargs)
    hosts = []
    for item in result["data"]["info"]:
        host_data = item["host"]
        ip = host_data["bk_host_innerip"]
        is_monitor = MonitorHost.objects.filter(ip=ip, biz_id=business_id).exists()

        hosts.append({
            "biz_id": business_id,
            "ip": ip,
            "system_name": host_data["bk_os_name"],
            "host_name": host_data["bk_host_name"],
            "cloud_name": host_data["bk_cloud_id"][0]["bk_inst_name"],
            "mem": "-",
            "disk": "-",
            "cpu": "-",
            "is_monitor": is_monitor,
            "btn_text": "移除监控" if is_monitor else "添加到监控",
        })

    return_data = {
        "catalogues": {
            "ip": "内网IP",
            "system_name": "系统名",
            "host_name": "主机名",
            "cloud_name": "云区域",
            "mem": "Mem(%)",
            "disk": "Disk(%)",
            "cpu": "CPU(%)",
        },
        "items": hosts
    }

    return render_json({"result": True, "data": return_data})
