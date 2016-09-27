#!/usr/bin/python
# -*- coding:utf-8 -*-
# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import re
from db.upload_datas import UplDatas
import math
from subscribe.models import *
from subscribe.pager import Pager
#import urllib2
import logging
logger = logging.getLogger('my')

@csrf_exempt
@login_required
def upload(request):    
    return render_to_response('upload.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
@login_required
def upload_space(request): 
    username = request.user.username
    page = int(request.GET.get('page', '1'))
    count = int(request.GET.get('count', '20'))
    
    inst = UplDatas.instance()
    video_list = inst.get_upload_video(username, page, count)
    #print video_list
    video_total = int(inst.get_upload_video_count(username))  
    
    page_count = int(math.ceil(float(video_total) / count))
    pg = Pager(page, page_count)
    page_list = pg.get_page_items()
       
    return render_to_response('upload_space.html', locals(), context_instance=RequestContext(request))
