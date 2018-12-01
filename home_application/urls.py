# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from home_application.api import test
from home_application.api import cmdb
from home_application.api import job
from home_application.api import monitor

urlpatterns = patterns(
    'home_application.views',
    (r'^$', 'home'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^api/test/$', test.test),
    (r'^api/search_business/$', cmdb.search_business),
    (r'^api/search_host/$', cmdb.search_host),
    (r'^api/get_host_mdc/$', job.get_host_mdc),
    (r'^api/add_host_monitor/$', monitor.add_host_monitor),
    (r'^api/remove_host_monitor/$', monitor.remove_host_monitor),
    (r'^api/search_m_host/$', monitor.search_m_host),
    (r'^api/get_monitor_data/$', monitor.get_monitor_data),
)
