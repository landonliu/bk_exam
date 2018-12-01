# -*- coding: utf-8 -*-
from common.mymako import render_json
from home_application.models import MonitorHost, MonitorHostData
from datetime import datetime, timedelta


def add_host_monitor(request):
    ip = request.GET.get("ip")
    biz_id = request.GET.get("business_id")
    MonitorHost.objects.create(ip=ip, biz_id=biz_id)
    return render_json({"result": True})


def remove_host_monitor(request):
    ip = request.GET.get("ip")
    biz_id = request.GET.get("business_id")
    MonitorHost.objects.filter(ip=ip, biz_id=biz_id).delete()
    MonitorHostData.objects.filter(ip=ip).delete()
    return render_json({"result": True})


def search_m_host(request):
    business_id = request.GET.get("business_id", "")
    body_data = request.body
    if not business_id:
        return render_json({"result": False, "message": "必须选择业务！"})
    ip_list_filter = body_data.split("\n")
    if len(ip_list_filter) == 0:
        data = MonitorHost.objects.filter(biz_id=business_id).values()
    else:
        data = MonitorHost.objects.filter(biz_id=business_id, ip__in=ip_list_filter).values()
    return render_json({"result": True, "data": list(data)})


def get_monitor_data(request):
    business_id = request.GET.get("business_id", "")
    ip = request.GET.get("ip", "")

    time_hour_ago = datetime.now() + timedelta(hours=-1)
    # time_hour_ago_str = time_hour_ago.strftime("%Y:%m:%d %H:%M:%S")

    if not business_id:
        return render_json({"result": False, "message": "必须选择业务！"})

    try:
        m_host = MonitorHost.objects.get(ip=ip, biz_id=business_id)

        m_data = MonitorHostData.objects.filter(ip=ip, time__gt=time_hour_ago)
        categories = []
        mem_data = {"color": "#f9ce1d",
                    "name": "mem",
                    "data": []}
        disk_data = {"color": "yellow",
                     "name": "disk",
                     "data": []}

        cpu_data = {"color": "red",
                    "name": "cpu",
                    "data": []}
        for item in m_data:
            categories.append(item.time.strftime("%Y-%m-%d %H:%M:%S"))
            mem_data["data"].append(item.mem)
            disk_data["data"].append(item.disk)
            cpu_data["data"].append(item.cpu)
    except MonitorHost.DoesNotExist as e:
        return render_json({"result": False})

    return_data = {
        "code": 0,
        "result": True,
        "messge": "success",
        "data": {
            "series": [mem_data, disk_data, cpu_data],
            "categories": categories
        }
    }

    return render_json(return_data)
