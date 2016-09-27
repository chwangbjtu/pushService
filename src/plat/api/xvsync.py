#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import re
import json
import urllib2
import urllib
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from db.xvsync_datas import XVsyncDatas

def del_xvsync(request):
    print request.GET
    try:
        ret = ''
        mid_1 = request.GET.get('mid_1','')
        mid_2 = request.GET.get('mid_2','')
        
        inst = XVsyncDatas.instance()
        ret = inst.del_xvsync(mid_1,mid_2)
        print ret
        if ret == ():
            ret = u'已删除！'
        else :
            ret = u'出错啦！'
        
        print ret
        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))