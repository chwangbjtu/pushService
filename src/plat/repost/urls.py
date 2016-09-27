#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns('',
    #url(r'^channellist/$', 'channel_list', name='channel_list'), 
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url channel_list %}
    
    url(r'^$', 'repost.views.repost', name = 'repost'),
    url(r'^repost$', 'repost.views.repost', name = 'repost'),
    url(r'^batch_repost$', 'repost.views.batch_repost', name = 'batch_repost'),
    url(r'^upload$', 'repost.views.upload_content', name = 'upload'),
    url(r'^repost_space$', 'repost.views.repost_space', name = 'repost_space'),
    
)
