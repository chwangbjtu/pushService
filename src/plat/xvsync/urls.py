#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns(('xvsync.views'),
    #url(r'^channellist/$', 'channel_list', name='channel_list'), 
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url channel_list %}
    
    url(r'^$', 'xvsync', name = 'xvsync'),
    url(r'xvsync$', 'xvsync', name = 'xvsync'),
    url(r'xv_show$', 'xv_show', name = 'xv_show'),
    url(r'media_details$', 'media_details', name = 'media_details'),
    url(r'video_show_tv$', 'video_show_tv', name = 'video_show_tv'),
    url(r'video_show_variaty$', 'video_show_variaty', name = 'video_show_variaty'),
    
    url(r'xv_edit$', 'xv_edit', name = 'xv_edit'),
    url(r'xv_edit_show$', 'xv_edit_show', name = 'xv_edit_show'),
    url(r'media_edit_details$', 'media_edit_details', name = 'media_edit_details'),
    
)
