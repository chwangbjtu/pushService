#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns(('subscribe.views'),
    #url(r'^channellist/$', 'channel_list', name='channel_list'), 
    # name属性是给这个url起个别名，可以在模版中引用而不用担心urls文件中url的修改 引用方式为{% url channel_list %}
    url(r'^$', 'youtube', name = 'subscribe'),
    
    url(r'^youtube/', 'youtube', name = 'youtube'),    
    
    url(r'^youku/', 'youku', name = 'youku'),

    url(r'keyword$', 'keyword', name = 'keyword'),
    url(r'keyword_show$', 'keyword_show', name = 'keyword_show'),
    url(r'keyword_add$', 'keyword_add', name = 'keyword_add'),
    
    url(r'^add/', 'add_order', name = 'add_order'),
    
    url(r'page$','page', name = 'page'),
    url(r'page_show$', 'page_show', name = 'page_show'),
    url(r'page_add$', 'page_add', name = 'page_add'),
    
    url(r'video$', 'video', name = 'video'),
    
    url(r"^welcome","welcome"),
    url(r"^navtree","nav_tree"),
    
    url(r'copyright_channel$', 'copyright_channel', name = 'copyright_channel'),
    url(r'copyright_channel_show$', 'copyright_channel_show', name = 'copyright_channel_show'),
    url(r'copyright_channel_add$', 'copyright_channel_add', name = 'copyright_channel_add'),
    
    url(r'cat$','cat', name = 'cat'),
    url(r'cat_show$', 'cat_show', name = 'cat_show'),
    url(r'cat_add$', 'cat_add', name = 'cat_add'),
    
    url(r'subject$','subject', name = 'subject'),
    url(r'subject_show$', 'subject_show', name = 'subject_show'),
    url(r'subject_add$', 'subject_add', name = 'subject_add'),

)
