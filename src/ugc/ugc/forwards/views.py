#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
import random
import time
from forms import UploadFileForm, BatchForwardForm
from models import Message2, BatchForwardResponse
import ugc.audit.audit_mgr.etc
import ugc.audit.audit_mgr.audit_mgr
import ugc.audit.audit_mgr.constant
import ugc.forwards.parse as parser
from ugc.audit.audit_mgr import pytools
import urllib
import urllib2
import json
import url_getid
import http_client
import etc
import constant

PSIZE = 20

PRIORITY_LIST = ("很低","低","中","高","很高")

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
            "distribute": "分发",
            "mediaserver":"分发中",
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
                #list_item[it] = status_dic[item[it]]
                pytools.show_value(item['step'], 'input_step_value')
                pytools.show_value(item[it], 'input_status_value')
                list_item[it] = get_map_status(item['step'], item[it])
            elif it == 'priority':
                list_item[it] = level_dic.get(item[it], '未知')
            else:
                list_item[it] = item[it]
        list.append(list_item)

    return list

def get_page(request):
    page = 1
    try:
        page = int(request.GET['page'])
    except Exception, e:
        print e
    return page

def get_data_list(code, res):
    data_list = []
    if code == ugc.audit.audit_mgr.constant.SUCCESS:
        try:
            for item in res:
                ret_json = json.loads(item)
                data_list.append(ret_json)
        except Exception,e:
            pytools.show_error(e)
    else:
        print 'get_tasklist error.'
    return data_list

def get_map_status(step, status):
    status_dic = {'0':'进行中','1':'完成','2':'失败','3':'未知'}

    if status == 2:
        return status_dic['2']
    elif status == 1:
        if step == 'videodown' or step == 'viper' or step == 'transcode' or step =='audit' or step =='mediaserver' or step == "distribute" or step == "submit":
            pytools.show_value(step,'step')
            pytools.show_value(status,'status')
            return status_dic['1']

    return status_dic['0']


@login_required
@permission_required("ugc.can_operate_forwards",login_url="/forbidden/")
def forwards_list(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)
    audit = ugc.audit.audit_mgr.audit_mgr.AuditMgr.instance()
    result = audit.get_forwards_userspace_v2(uid,pagesize,page)
    if result[0] == ugc.audit.audit_mgr.constant.SUCCESS:
        code = result[0]
        record_count = result[1]
        res = result[2]
    else:
        code = ugc.audit.audit_mgr.constant.FAIL
        record_count = 0
        res = None
    data_list = map_data_list(get_data_list(code, res))

    return forwards_list_page(data_list, record_count, page, pagesize)

def forwards_list_page(data_list, record_count, page_number, pagesize):
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('forwards_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'page_count':page_count})


@login_required
@permission_required("ugc.can_operate_forwards",login_url="/forbidden/")
def forwards_page(request):
    #return render_to_response("upload/upload.html",{"priority_list":PRIORITY_LIST})
    return forwards(request)



def get_vid_from_url(url):
    try:
        urltoid = url_getid.UrlToId()
        (flag, urlwebtype, vid) = urltoid.urlgetid(url)
        if flag != constant.SUCCESS:
            print 'not success with: ', url
            return (None, None)
        print urlwebtype, vid
        return (urlwebtype,vid)
    except Exception,e:
        print 'get_vid_from_url error',e
        return (None, None)

def send_taskmgr_pack(tid, vid, origin, site, priority):
    try:
        json_values = {'tid':tid, 'vid':vid, 'origin':origin, 'site':site, 'priority':priority,}
        taskmgr_str = json.dumps(json_values)
        (code, res) = http_client.post(etc.task_mgr_ip, etc.task_mgr_port, etc.task_mgr_method, taskmgr_str)
        if code != 200:
            return False
        return True
    except Exception,e:
        print 'produce_taskmgr_pack error: ', e
        return False

@login_required
def forwards(request):
    if request.method == 'POST' and request.POST.__contains__("single"):
        print request.POST
        print 'web forwards POST'
        form = UploadFileForm(request.POST)
        the_page = None
       
        if form.is_valid():
            url = form.cleaned_data['url']
            title = form.cleaned_data['title']
            tag = form.cleaned_data['tag']
            description = form.cleaned_data['description']
            level = form.cleaned_data['level']
            channel = form.cleaned_data['channel']
            uid = request.user.id

            (site, vid) = get_vid_from_url(url)
            if vid == None:
                return render_to_response('upload.html', {'form': form, 'batch': BatchForwardForm(), 'trips':"输入的url无法解析!", 'batch_mode': False})

            values = {'uid' : uid,'vid':vid, 'site' : site,'title' : title,'describe' : description,'tags' : tag,'channel' : channel,'origin' : 'forwards','priority' : level,}

            send_maze_str = json.dumps(values)

            the_page = http_client.postmaze_get_tid(etc.maze_service_ip, etc.maze_service_port, etc.maze_newtask_method, send_maze_str)
            if the_page == None:
                return render_to_response('upload.html', {'form': form, 'batch': BatchForwardForm(), 'trips':"网络超时", 'batch_mode': False})
            print 'return from maze: ', the_page
        if the_page != None:
            ret_dic = json.loads(the_page)
            if ret_dic['result'] == 'ok':
                tid = ret_dic['tid']
                data = []
                message = Message2()
                message.key         = "tid"
                message.key_value   = "任务ID"
                message.title_value = tid# "提交成功"
                message.title       = tid 
                data.append(message)
                form = UploadFileForm()
                return render_to_response('detailrefresh.html', {'form':form, 'batch': BatchForwardForm(), 'data':data, 'batch_mode': False})
            else:
                return render_to_response('upload.html', {'form': form, 'batch': BatchForwardForm(),'trips':"url 输入不能匹配，程序不能处理", 'batch_mode': False})
        else:
            return render_to_response('upload.html', {'form': form, 'batch': BatchForwardForm(), 'batch_mode': False})
    elif request.method == 'POST' and request.POST.__contains__("batch"):
        print request.POST
        form = UploadFileForm()
        batch = BatchForwardForm(request.POST)
        link_map = {}
        data = []
        failed = []
        if batch.is_valid():
            links       = batch.cleaned_data['links']
            level       = batch.cleaned_data['level']
            link_list = links.split('\n')
            
            for link in link_list:
                link = link.strip()
                if link:
                    link_map[link] = link
            if  len(link_map) > 100:
                for link in link_map:
                    message = BatchForwardResponse()
                    message.link = link
                    failed.append(message)
                return render_to_response('upload.html', {'form': form, 'batch': batch, 'trips':"url数目超出了限制", 'batch_mode': True})
                
            for link in link_map:
                link_map[link] = parser.parse_one_url(link)

            for link in link_map:
                message = BatchForwardResponse()
                message.link = link
                if not link_map[link]:
                    message.response = 'fail'
                    failed.append( message )
                    continue
                (site, vid) = get_vid_from_url(link)
                if vid == None or not site :
                    message.response = 'fail'
                    failed.append( message )
                    continue
                link_map[link]['uid'] = request.user.id
                link_map[link]['site'] = site
                link_map[link]['vid']  = vid
                link_map[link]['origin'] = 'forwards'
                link_map[link]['priority'] = level 
                link_map[link]['channel'] = site if not link_map[link]['channel'].strip() else  link_map[link]['channel'].strip()               
                link_map[link]['tags'] = link_map[link]['tag'].replace(',', '|') 
                link_map[link]['describe'] = link_map[link]['description']  
                the_page = http_client.postmaze_get_tid(etc.maze_service_ip, etc.maze_service_port, etc.maze_newtask_method, json.dumps(link_map[link]))
                
                if the_page and json.loads(the_page)['result'] == 'ok':
                    message.response = 'ok'
                    data.append( message )
                else:
                    message.response = 'fail'
                    failed.append( message )
            return render_to_response('batch_forward_result.html', {'batch_data':data, 'batch_data_failed': failed, 'batch_mode': True})
        return render_to_response('upload.html', {'form': form, 'batch': batch, 'batch_mode': True})        
    else:
        form = UploadFileForm()
        batch = BatchForwardForm()
        return render_to_response('upload.html', {'form': form, 'batch': batch, 'batch_mode': False})

def forwards_detail(request):
    global MAP_DIC
    show_dic = MAP_DIC
    tid = request.GET['tid']
    test_url,the_page = get_tid_status(tid)
    data = []
    for item in the_page:
        message = Message2()
        if item in show_dic.keys():
            message.key = item
            message.key_value = show_dic[item]['key_value']
            message.title = the_page[item]
            title = the_page[item]
            if title in show_dic[item].keys():
                message.title_value = show_dic[item][title]
            else:
                message.title_value = the_page[item]
            if item == 'status' and title == 2:
                data.append(message)
            elif item =='url' and title != None:
                data.append(message)
            elif item != 'status' and item != 'url':
                data.append(message)
        else:
            message.key = item
            message.title = the_page[item]
            data.append(message)

    return render_to_response('detailrefresh.html', {'data': data})

def get_tid_status(tid):
    dic = {}
    dic['tid'] = str(tid)
    param = urllib.urlencode(dic)
    test_url = "%s?%s" % (ugc.audit.audit_mgr.etc.status_service, param)
    _opener = urllib2.build_opener()
    response = _opener.open(test_url, timeout = 60)
    the_page = response.read()
    print '2....', the_page
    ret = paster_str(the_page)
    return (test_url, ret)

def paster_str(cont):
    stat_dic = None
    stat_list = json.loads(cont)
    for item in stat_list:
        stat_str = item
        stat_dic = json.loads(stat_str)
    return stat_dic

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
