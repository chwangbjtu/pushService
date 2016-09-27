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
from db.db_datas import DBDatas
import math
from subscribe.pager import Pager
import urllib2
import logging
logger = logging.getLogger('my')

@csrf_exempt
@login_required
def douban(request):
    classifi = request.GET.get('classifi', '').encode("utf8")
    order = request.GET.get('order','').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")
    
    video_dao = DBDatas.instance()
    video_list = video_dao.get_douban_video(page, count, classifi, order, cond, content)
    video_total = int(video_dao.get_douban_video_count(classifi, cond, content))
    #print video_total
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    category_item = [['',u'所有分类'],['1',u'电影'],['2',u'电视剧'],['3',u'综艺'],['4',u'动漫']]
    classifi_item = category_item
    order_item = [['',u'排序方式'],['score',u'评分']]
    search_item = [['',u'搜索类型'],['title',u'标题'],['type',u'类型']]
    
    return render_to_response('douban.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def fun_db(request):
    disable = request.GET.get('disable', '').encode("utf8")
    status = request.GET.get('status','').encode("utf8")
    order = request.GET.get('order','').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")
    
    video_dao = DBDatas.instance()
    video_list = video_dao.get_FunDB_video(page, count, disable, status, order, cond, content)
    video_total = int(video_dao.get_FunDB_video_count(disable, status, cond, content))
    #print video_total
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    disable_item = [['',u'所有'],['0',u'可播放'],['1',u'不可播']]
    status_item = [['',u'所有状态'],['0',u'初始'],['1',u'已编辑'],['2',u'被踢除']]
    order_item = [['',u'排序'],['0',u'匹配度']]
    #search_item = [['',u'搜索类型'],['name',u'风行title'],['title',u'豆瓣title'],['category',u'风行分类']]
    search_item = [['',u'搜索类型'],['name',u'风行title'],['title',u'豆瓣title']]

    return render_to_response('fun_db.html',locals(),context_instance=RequestContext(request))

@csrf_exempt
@login_required
def fun_details(request):
    rel_id = request.GET.get('id','')
    media_id = request.GET.get('media_id','')
    show_id = request.GET.get('show_id','')

    fun_detail = {}
    dou_detail = {}

    xv_dao = DBDatas.instance()
    if media_id:
        fun_detail = xv_dao.get_funshion_detail(media_id)
    if show_id:
        dou_detail = xv_dao.get_douban_detail(show_id)
    
    return render_to_response('fun_details.html', {'rel_id': rel_id, 'fun_detail': fun_detail, 'dou_detail': dou_detail}, context_instance=RequestContext(request))
