#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ugc.audit.audit_mgr import audit_mgr
from ugc.audit.audit_mgr import constant

import json

MAP_DIC = {
        "tid":{"key_value":"任务ID","title":"title","title_value":"title_value"},
        "url":{"key_value":"链接","title":"title","title_value":"title_value"},
        "step":{"key_value":"流程环节",
            "spider":"上传中",
            "forwards":"上传中",
            "upload":"上传中",
            "parser":"上传中",
            "taskmanager":"上传中",
            "videodown":"上传中",
            #上传中
            "viper":"等待转码",
            #等待转码
            "submit":    "提交",
            "transcode": "转码",
            "audit":     "审核",
            "mpacker":   "打包",
            "distribute":"分发",
            #审核中
            "mediaserver":"分发中",
            "macros":"分发中",
            #完成
            "title_value":"title_value"},
        "status":{"key_value":"状态",1:"完成",0:"进行中",2:"失败"},
        }


LEVEL_CHOICES = {
3: '很低',
4: '低',
5: '中',
6: '高',
7: '很高',
}

def get_page(request):
    page = 1
    try:
        page = int(request.GET['page'])
    except Exception, e:
        print e
    return page

def get_pagecount(code, res):
    record_count = 0
    if code == constant.SUCCESS:
        record_count = res
    else:
        print 'get total number error.'
    return record_count

def map_data_list(data_list):
    global MAP_DIC
    global LEVEL_CHOICES
    show_dic = MAP_DIC
    step_dic = show_dic['step']
    status_dic = show_dic['status']
    level_dic = LEVEL_CHOICES

    list = []
    for item in data_list:
        list_item = {}
        for it in item:
            if it == 'step':
                list_item[it] = step_dic[item[it]]
            elif it == 'status':
                list_item[it] = status_dic[item[it]]
            elif it == 'priority':
                list_item[it] = level_dic[item[it]]
            else:
                list_item[it] = item[it]
        list.append(list_item)

    return list

def get_data_list(code, res):
    data_list = []
    if code == constant.SUCCESS:
        try:
            for item in res:
                ret_json = json.loads(item)
                data_list.append(ret_json)
        except Exception,e:
            audit_mgr.pytools.show_error(e)
    else:
        print 'get_tasklist error.'
    return data_list

@login_required
def upload_list(request):
    pagesize = 10
    uid = request.user.id
    page = get_page(request)
    audit = audit_mgr.AuditMgr.instance()
    result = audit.get_forwards_userspace_v2(uid,pagesize,page,"upload")
    if result[0] == constant.SUCCESS:
        code = result[0]
        record_count = result[1]
        res = result[2]
    else:
        code = constant.FAIL
        record_count = 0
        res = None
    data_list = map_data_list(get_data_list(code, res))

    return forwards_list_page(data_list, record_count, page, pagesize)

def list_info(record_count,pagesize,page_number):
    range_start = 0
    range_end = 0
    radii = 7
    start = 1+ page_number - radii
    end = page_number + radii
    page_count = int(record_count / pagesize) + 1

    if  start > 1:
        range_start = start
    else:
        range_start = 1
    if end < page_count + 1:
        range_end = end
    else:
        range_end = page_count + 1

    page_range = range(range_start, range_end)
    page_number_last = int(page_number) - 1
    page_number_next = int(page_number) + 1
    return page_range, page_count, page_number_last, page_number_next

def forwards_list_page(data_list, record_count, page_number, pagesize):
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('upload/upload_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'page_count':page_count})