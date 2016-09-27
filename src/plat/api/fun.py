#!/usr/bin/python
# -*- coding:utf-8 -*-

#from django.shortcuts import render
from django.http import StreamingHttpResponse
from db.db_datas import DBDatas
from django.views.decorators.csrf import csrf_exempt
from plat.common import cal_fit
import json
#import time
import logging
logger = logging.getLogger('my')

# Create your views here. 
@csrf_exempt   
def edit_fun(request,op):
    username = request.user.username
    try:
        ret = ""
        id = request.GET.get('id')
        media_id = request.GET.get('media_id')
        name = request.GET.get('name')
        director = request.GET.get('director')
        actor = request.GET.get('actor')
        category = request.GET.get('category')
        show_id = request.GET.get('show_id')
        
        #print op, media_id, name, director, actor
        fun = DBDatas.instance()

        #calculate fit
        if op == "replace":
            ret = fun.update_fun_db(id, media_id, name, director, actor, category)
            
            douban_detail = fun.get_douban_detail(show_id)
            fun_detail = fun.get_funshion_detail(media_id)
            fit = cal_fit(fun_detail, douban_detail)
            fun.update_fun_dou_fit(media_id, show_id, fit)
            logger.info(u"用户:%s 修复了风行数据，风行ID:%s, 豆瓣ID:%s",username,media_id,show_id)
            
        if op == "eliminate":
            ret = fun.eliminate_fun_db(id)
            
            logger.info(u"用户:%s 执行了剔除操作，风行ID:%s, 豆瓣ID:%s",username,media_id,show_id)

        #print ret
        if not ret:
            ret = "ok"
        #print ret
        return StreamingHttpResponse(json.dumps({'ret': ret}))
    except Exception, e:
        print e
        return StreamingHttpResponse(json.dumps({'ret': 'operation error: %s' % e}))

'''
@csrf_exempt    
def funid(request):
    try:
        ret = ""
        #print request.GET
        id = request.GET.get('id')
        media_id = request.GET.get('media_id')
        
        funid = DBDatas.instance()
        ret = funid.get_funid_video(id, media_id)
        
        return StreamingHttpResponse(json.dumps({'ret': '0', 'data': ret, 'row_id': id}))
    except Exception, e:
        print e
        return StreamingHttpResponse(json.dumps({'ret': '1', 'msg': 'operation error: %s' % e}))
'''
