#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns(('blacklist.views'),
    #url(r'^channellist/$', 'channel_list', name='channel_list'), 
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url channel_list %}
    
    url(r'^$', 'blacklist', name = 'blacklist'),
    url(r'blacklist$', 'blacklist', name = 'blacklist'),
    url(r'blacklist_copyright$', 'blacklist_copyright', name = 'blacklist_copyright'),
    url(r'blacklist_politic$', 'blacklist_politic', name = 'blacklist_politic'),
    url(r'blacklist_add$', 'blacklist_add', name = 'blacklist_add'),
    #url(r'fun_details$', 'fun_details', name = 'fun_details'),
    
)
