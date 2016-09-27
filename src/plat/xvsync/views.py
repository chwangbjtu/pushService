#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import re
from django.db import connection
from itertools import chain
from db.xvsync_datas import XVsyncDatas
import math
from subscribe.pager import Pager
from plat.settings import POSTERS_PATH
import urllib2
import logging
logger = logging.getLogger('my')

#site_item = {10:u'优酷', 11:u'土豆', 12:u'腾讯',13:u'搜狐', 14:u'爱奇艺', 15:u'乐视', 16:u'1905', 17:u'迅雷', 18:u'芒果TV', 50:u'风行', 60:u'360'}
inst = XVsyncDatas.instance()
site_item2 = list(inst.get_site())
site_dict = {}
for site in site_item2:
    site_dict[site["site_id"]] = site["repr"]
#使用site_dict代替原来的site_item，这样网站代码和网站从数据库中读取，不用在代码中写死了
search_ITEM = [['title', u'标题']]
screen_ITEM = [['1', u'耦合'], ['2', u'未耦合'], ['3', u'所有']]

@login_required
def xvsync(request):
    search_item = search_ITEM
    screen_item = screen_ITEM
    #print request.GET
    search_cond = request.GET.get('cond','title')
    search_content = request.GET.get('content','')
    screen = request.GET.get('screen','1')
    channel_id = request.GET.get('channel_id','2001')
    page = request.GET.get('page','1')
    #print search_cond,search_content,screen
    return render_to_response("xvsync.html",locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def xv_show(request):
    #print request.GET
    #print request.POST
    username = request.user.username
    page = int(request.POST.get('page', '1'))
    count = int(request.POST.get('count', '30'))
    channel_id = request.POST.get('channel_id', '2001')
    cond = request.POST.get('cond','title')
    content = request.POST.get('content','')
    screen = request.POST.get('screen','')
    #print cond,content    
    
    inst = XVsyncDatas.instance()
    video_list = inst.get_xvsync_list(page, count, channel_id, cond, content, screen)
    #print video_list
    video_total = int(inst.get_xvsync_list_count(channel_id, cond, content, screen))  
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    posters_path = POSTERS_PATH
    
    return render_to_response("xv_show.html", locals(), context_instance=RequestContext(request))

def media_details(request):#偶合页媒体详情
    #print request.GET
    posters_path = POSTERS_PATH
    
    mid = request.GET.get('mid','')
    channel_id = request.GET.get('channel_id','')
    
    mid_site_list = ''
    inst = XVsyncDatas.instance()
    xv_detail = inst.get_xvsync_details(mid)
    mid_site_list = list(inst.get_mid_site(mid))#将得到的tuple类型转化为list类型，方便将没有URL的元素删除
    #print mid_site_list
    
    for video in mid_site_list:
        video['site'] = site_dict[video['site_id']]
        
    list0 = []        
    if channel_id == '2001':
        for video in mid_site_list:
            url0 = inst.get_xvsync_movie(video['mid'])
            if url0==None:
                list0.append(video)
                #不能在此时将元素删除，否则会导致有一个元素无法遍历到；所以放在后面删除
                continue
            video['url'] = url0['url']
    
    for video in list0:
        mid_site_list.remove(video)
        
    return render_to_response("media_details.html", locals(), context_instance=RequestContext(request))

@csrf_exempt    
def video_show_tv(request):#电视剧、动漫耦合页，耦合媒体的展示
    username = request.user.username
    mid = request.POST.get('mid', '')
    
    inst = XVsyncDatas.instance()
    video_list = inst.get_xvsync_tv(mid)
    
    return render_to_response("video_show_tv.html", locals(), context_instance=RequestContext(request))

@csrf_exempt    
def video_show_variaty(request):#综艺耦合页，耦合媒体的展示
    username = request.user.username
    mid = request.POST.get('mid', '')
    
    inst = XVsyncDatas.instance()
    video_list = inst.get_xvsync_variaty(mid)
    
    return render_to_response("video_show_variaty.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def xv_edit(request):
    search_item = search_ITEM
    screen_item = screen_ITEM
    #print request.GET
    search_cond = request.GET.get('cond','title')
    search_content = request.GET.get('content','')
    screen = request.GET.get('screen','3')
    channel_id = request.GET.get('channel_id','2001')
    page = request.GET.get('page','1')
    #print request.GET
    return render_to_response("xv_edit.html", locals(), context_instance=RequestContext(request))

@csrf_exempt
def xv_edit_show(request):
    #print request.GET
    #print request.POST
    username = request.user.username
    page = int(request.POST.get('page', '1'))
    count = int(request.POST.get('count', '50'))
    channel_id = request.POST.get('channel_id', '2001')
    cond = request.POST.get('cond','title')
    content = request.POST.get('content','') 
    screen = request.POST.get('screen','')   
    
    inst = XVsyncDatas.instance()
    video_list = inst.get_xvsync_list(page, count, channel_id, cond, content, screen)
    #print video_list
    video_total = int(inst.get_xvsync_list_count(channel_id, cond, content, screen))  
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    posters_path = POSTERS_PATH
    
    return render_to_response("xv_edit_show.html", locals(), context_instance=RequestContext(request))

def media_edit_details(request):
    #print request.GET
    posters_path = POSTERS_PATH
    
    mid = request.GET.get('mid','')
    channel_id = request.GET.get('channel_id','')
    
    mid_site_list = ''
    inst = XVsyncDatas.instance()
    xv_detail = inst.get_xvsync_details(mid)
    mid_site_list = list(inst.get_mid_site(mid))
    #print mid_site_list
    
    for video in mid_site_list:
        video['site'] = site_dict[video['site_id']]

    list0 = []
    if channel_id == '2001':
        for video in mid_site_list:
            url0 = inst.get_xvsync_movie(video['mid'])
            if url0==None:
                list0.append(video)
                continue
            video['url'] = url0['url']

    for video in list0:
        mid_site_list.remove(video)
    
    return render_to_response("media_edit_details.html", locals(), context_instance=RequestContext(request))


    