#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns(('video_house.views'),
    #url(r'^channellist/$', 'channel_list', name='channel_list'), 
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url channel_list %}
    
    url(r'^$', 'douban', name = 'douban'),
    url(r'douban$', 'douban', name = 'douban'),
    url(r'fun_db$', 'fun_db', name = 'fun_db'),
    url(r'fun_details$', 'fun_details', name = 'fun_details'),
    
)
