#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import StreamingHttpResponse
import json
from db.blacklist_datas import BLDatas
import httplib
import urllib2
from plat.settings import DATA_SERVER_IP, DATA_SERVER_PORT

def add_blacklist(request):
    username = request.user.username
    try:
        ret = ''
        bl_word = request.GET.get('bl_word', '')
        bl_type = request.GET.get('bl_type', '')
        #print bl_word,bl_type
        
        inst = BLDatas.instance()
        ret = inst.add_blacklist(bl_word,bl_type)

        #send to data server
        try:
            url = "/op/updateblacklist?op=add&content=%s" % (urllib2.quote(bl_word.encode('utf8')),)
            conn = httplib.HTTPConnection(DATA_SERVER_IP, DATA_SERVER_PORT)
            conn.request('GET', url)
            ret = "ok"
        except Exception, e:
            ret = str(e)
            print ret

        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))
    
def del_blacklist(request):
    username = request.user.username
    try:
        #print request.POST
        #print request.GET
        bl_id = request.GET.get('bl_id', '')
        #print bl_id
        
        inst = BLDatas.instance()
        ret = inst.del_blacklist(bl_id)
        ret = 'ok'
        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))
    
