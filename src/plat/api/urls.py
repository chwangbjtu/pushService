#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *


urlpatterns = patterns('',
    url(r'^subscribe/keyword/(?P<op>.+)/$', 'api.handler.subscribe_keyword', name='keyword_api'),
    url(r'^subscribe/keyword/(?P<op>.+)$', 'api.handler.subscribe_keyword', name='keyword_api'),
    
    url(r'^subscribe/page/(?P<op>.+)/$', 'api.handler.subscribe_page', name='page_api'),
    url(r'^subscribe/page/(?P<op>.+)$', 'api.handler.subscribe_page', name='page_api'),

    url(r'^parse/$', 'api.parse.parse_url'),
    url(r'^parse$', 'api.parse.parse_url'),
    
    url(r'^cc/(?P<op>.+)/$','api.copyright_channel.cc'),
    url(r'^cc/(?P<op>.+)$','api.copyright_channel.cc'),
    
    url(r'^subscribe/cat/(?P<op>.+)/$', 'api.handler.subscribe_cat', name='cat_api'),
    url(r'^subscribe/cat/(?P<op>.+)$', 'api.handler.subscribe_cat', name='cat_api'),
    
    url(r'^subscribe/subject/(?P<op>.+)/$', 'api.handler.subscribe_subject', name='subject_api'),
    url(r'^subscribe/subject/(?P<op>.+)$', 'api.handler.subscribe_subject', name='subject_api'),

    url(r'^send/episode/$', 'api.handler.send_episode', name='send_episode'),
    url(r'^send/episode$', 'api.handler.send_episode', name='send_episode'),
    
    url(r'^subscribe/fun/(?P<op>.+)/$', 'api.fun.edit_fun', name='fun_api'),
    url(r'^subscribe/fun/(?P<op>.+)$', 'api.fun.edit_fun', name='fun_api'),
    
    #url(r'^subscribe/funid/$', 'api.fun.funid', name='funid_api'),

    url(r'^fix/funshion/$', 'api.handler.fix_funshion', name='fix_funshion'),
    url(r'^fix/funshion$', 'api.handler.fix_funshion', name='fix_funshion'),
    
    url(r'^blacklist/add/$', 'api.blacklist.add_blacklist', name='add_blacklist'),
    url(r'^blacklist/add$', 'api.blacklist.add_blacklist', name='add_blacklist'),
    
    url(r'^blacklist/del/$', 'api.blacklist.del_blacklist', name='del_blacklist'),
    url(r'^blacklist/del$', 'api.blacklist.del_blacklist', name='del_blacklist'),
    
    url(r'^xvsync/del/$', 'api.xvsync.del_xvsync', name='del_xvsync'),    
    url(r'^xvsync/del$', 'api.xvsync.del_xvsync', name='del_xvsync'),    
)
