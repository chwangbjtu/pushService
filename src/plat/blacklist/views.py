#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import re
#from django.db import connection
#from itertools import chain
from db.blacklist_datas import BLDatas
import math
from subscribe.models import *
from subscribe.pager import Pager
#import urllib2
import logging
logger = logging.getLogger('my')

@csrf_exempt
@login_required
def blacklist(request):    
    return render_to_response('blacklist.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def blacklist_copyright(request): 
    #bls = Blacklist.objects.filter(type=0)   
    classifi = request.GET.get('classifi', '').encode("utf8")
    order = request.GET.get('order','').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")
    
    video_dao = BLDatas.instance()
    video_list = video_dao.get_blcr_video(page, count)
    video_total = int(video_dao.get_blcr_video_count())
    #print video_total
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
    
    return render_to_response('blacklist_copyright.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def blacklist_politic(request): 
    #bls = Blacklist.objects.filter(type=1)
    classifi = request.GET.get('classifi', '').encode("utf8")
    order = request.GET.get('order','').encode("utf8")
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    cond = request.GET.get('cond','').encode("utf8")
    content = request.GET.get('content','').encode("utf8")
    
    video_dao = BLDatas.instance()
    video_list = video_dao.get_blpl_video(page, count)
    video_total = int(video_dao.get_blpl_video_count())
    #print video_total
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
        
    return render_to_response('blacklist_politic.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def blacklist_add(request):    
    return render_to_response('blacklist_add.html', locals(), context_instance=RequestContext(request))
