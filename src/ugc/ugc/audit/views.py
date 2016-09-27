#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from audit_mgr import audit_mgr
from audit_mgr import etc
from audit_mgr import constant
from audit_mgr import pytools
from forms import UploadFileForm
from models import Message2

import urllib
import urllib2
import json
PSIZE = 20

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
            "submit":    "提交",
            "transcode": "转码",
            "audit":     "审核",
            "mpacker":   "打包",
            "distribute":"分发",
            
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

def get_search_list():
    search_list = [
                ("tid","视频ID"),
                ("vid","vid"),
                ("title","标题"),
                ("tags","标签"),
                ]
    return search_list

def get_order_list():
    order_list = [
                ("time","按时间"),
                ("time desc","按时间逆序"),
                ("tid","按视频ID"),
                ("tid desc","按视频ID逆序"),
                ]
    return order_list

def get_real_cols():
    cols = [
            ("tuiding_col","退订"),
            ("tid_col","视频ID"),
            ("uid_col","用户ID"),
            ("title_col","标题"),
            ("tags_col","标签"),
            ("channel_col","频道"),
            ("funshion_id_col","风行ID"),
            ("user_col","上传用户"),
            ("duration_col","时长"),
            ("playtimes_col","播放量"),
            ("username_col","审核用户"),
            ("time_col","审核时间"),
            ("vid_col","vid"),
            ("priority_col","优先级"),
            ("action_col","操作"),
    ]
    return cols

@login_required
def home_page(request):
    return render_to_response("index.html",{})

@login_required
def nav_tree(request):
    perm_list =(    "can_operate_audit_space",
                    "can_access_manage_space",
                    "can_access_global_space",
                    "can_operate_forwards",
                    "can_show_audit",
                    "can_operate_upload")
    args = {"username":request.user.username}
    for item in perm_list:
        perm_name = "ugc.%s" % item
        if request.user.has_perm(perm_name):
            args[item] = True
        else:
            args[item] = False
    return render_to_response("nav_tree.html",args)

@login_required
def welcome(request):
    return render_to_response("welcome.html",{})

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

def get_data_list(code, res):
    data_list = []
    if code == constant.SUCCESS:
        try:
            for item in res:
                ret_json = json.loads(item)
                data_list.append(ret_json)
        except Exception,e:
            pytools.show_error(e)
    else:
        print 'get_tasklist error.'
    return data_list

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
                list_item[it] = get_map_status(item['step'], status_dic[item[it]])
            elif it == 'priority':
                print 'priority is %s' % item[it]
                list_item[it] = level_dic.get(item[it], '低')
            else:
                list_item[it] = item[it]
        list.append(list_item)

    return list

def get_map_status(step, status):
    pytools.show_value(status, 'status')
    status_dic = {'0':'进行中','1':'成功','2':'失败'}
    if status == 2:
        return status_dic['2']
    elif status == 1:
        if step == 'videodown' or step == 'viper' or step == 'transcode' or step =='macros':
            return status_dic['1']

    return status_dic['0']

def get_tid_status(tid):
    dic = {}
    dic['tid'] = str(tid)
    param = urllib.urlencode(dic)
    test_url = "%s?%s" % (etc.status_service, param)
    _opener = urllib2.build_opener()
    response = _opener.open(test_url, timeout = 60)
    the_page = response.read()
    ret = paster_str(the_page)
    return (test_url, ret)

def paster_str(cont):
    stat_dic = None
    stat_list = json.loads(cont)
    for item in stat_list:
        stat_str = item
        stat_dic = json.loads(stat_str)
    return stat_dic

@login_required
@permission_required("ugc.can_access_manage_space",login_url="/forbidden/")
def user_count(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)
    audit = audit_mgr.AuditMgr.instance()
    data_list= []
    record_count = 0
    start_date = ""
    end_date = ""
    tips = ""

    import time
    new_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    end_date = new_date
    start_date = new_date

    if ('end' in request.GET):
        end_date = request.GET['end']

    if ('start' in request.GET):
        start_date = request.GET['start']
    
    #record_count = res
    #record_count：审核人数，　audit_total_num 审核总数
    (code, record_count, res, total_list) = audit.get_audit_statics_info(start_date, end_date, pagesize, page)

    data_list = res
    if end_date < start_date:
        tips = "输入的开始时间比截止时间还要大，所以数据库没有能查询到信息。"

    return user_count_page(data_list, record_count, page, pagesize, start_date, end_date,tips)

@login_required
@permission_required("ugc.can_access_global_space",login_url="/forbidden/")
def admin_all_video(request):
    pagesize = PSIZE
    uid = request.user.id
    uid = -1
    page = get_page(request)
    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_all_tasklist(uid, -1, 1, data_dic)
    #record_count = get_pagecount(code, res)

    (code, record_count, res) = audit.get_all_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)
    return admin_audit_all_list_page(data_list, record_count, page, pagesize, page_info)

def get_data_dic(request):
    data_dic={}
    search_str = ''
    order_str = ''
    pytools.show_value(request.GET,'request.GET')

    search_category = request.GET.get('search','')
    if search_category: 
        search_content = request.GET.get('search_content','')
        if search_content:
            search_str = '%s like "%%%s%%"' %(search_category, search_content.strip())
            data_dic['search'] = search_str

    #pytools.show_value(search_str,'search_str')

    order_item = request.GET.get('order','')
    #pytools.show_value(order_item,'order_item')
    if order_item:
        order_str = ' %s' % order_item
        data_dic['order'] = order_str

    #pytools.show_value(order_str,'order_str')

    return data_dic

def get_cols_str(request):
    cols = get_set_form_col(request)
    cols_str = ''
    for col in cols:
        cols_str = cols_str + '&' + 'm=' + col

    return cols_str

def get_page_info(request):
    page_info = {}
    page_info['search'] = request.GET.get('search','')
    page_info['search_content'] = request.GET.get('search_content','')
    page_info['order'] = request.GET.get('order','')

    cols = get_set_form_col(request)
    page_info['cols'] = cols
    page_info['cols_real'] = get_real_cols()
    col_str = get_cols_str(request)
    request_args = "&search=%s&search_content=%s&order=%s%s" % (page_info.get('search',''),page_info.get('search_content',''),page_info.get('order',''), col_str)

    page_info['request_args'] = request_args

    return page_info

def get_col_name():
    return 'm'

def get_set_form_col(request):
    cols = []
    get_dic = {}
    cols = request.GET.getlist('m','')
    pytools.show_value(cols, 'cols')

    return cols

@login_required
@permission_required("ugc.can_access_global_space",login_url="/forbidden/")
def admin_pending_video(request):
    pagesize = PSIZE
    uid = request.user.id
    uid = -1
    page = get_page(request)
    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_pending_tasklist(uid, -1, page,data_dic)
    #record_count = get_pagecount(code, res)
    #(code, res) = audit.get_pending_tasklist(uid, pagesize, page,data_dic)
    (code, record_count, res) = audit.get_pending_tasklist(uid, pagesize, page,data_dic)
    data_list = get_data_list(code, res)

    return admin_audit_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_access_global_space",login_url="/forbidden/")
def admin_passed_video(request):
    pagesize = PSIZE
    uid = request.user.id
    uid = -1
    page = get_page(request)
    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_passed_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_passed_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    return admin_audit_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_access_global_space",login_url="/forbidden/")
def admin_failure_video(request):
    pagesize = PSIZE
    uid = request.user.id
    uid = -1
    page = get_page(request)

    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_failure_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_failure_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    return admin_audit_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_access_manage_space",login_url="/forbidden/")
def distribute_video_count(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)
    audit = audit_mgr.AuditMgr.instance()
    data_list= []
    record_count = 0
    start_date = ""
    end_date = ""
    tips = ""

    import time
    new_date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    end_date = new_date
    start_date = new_date

    if ('end' in request.GET):
        end_date = request.GET['end']

    if ('start' in request.GET):
        start_date = request.GET['start']

    pytools.show_value(start_date, 'start_date')
    pytools.show_value(end_date, 'end_date')
    (code, res1, res2) = audit.get_dat_macros_statics_list(start_date, end_date, pagesize, page)
    pytools.show_value(code, 'code')
    pytools.show_value(res1, 'res1')
    pytools.show_value(res2, 'res2')

    record_count = res1

    data_list = res2
    pytools.show_value(type(res2),'res2 type')
    if end_date < start_date:
        tips = "输入的开始时间比截止时间还要大，所以数据库没有能查询到信息。"

    return distribute_list_page(data_list, record_count, page, pagesize, start_date, end_date,tips)

@login_required
@permission_required("ugc.can_access_manage_space",login_url="/forbidden/")
def distribute_video_search(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)

    data_dic= get_data_dic(request)
    pytools.show_value(data_dic, 'data_dic')
    page_info = get_page_info(request)
    pytools.show_value(page_info, 'page_info')

    audit = audit_mgr.AuditMgr.instance()

    key_search = page_info.get('search_content','')
    key_type = page_info.get('search','')
    #code, ret, ret2 = audit.search_mp4_info_from_dat(key_search, key_type, pagesize, page)
    retall = audit.search_mp4_info_from_dat(key_search, key_type, pagesize, page)
    pytools.show_value(retall, 'retall')
    code = retall[0]
    pytools.show_value(code, 'code')
    if code > 0:
       ret = retall[1]
       ret2 = retall[2]
    else:
       ret = 0
       ret2 = None
    pytools.show_value(ret, 'ret')
    record_count = ret
    data_list = ret2

    return search_distribute_video_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def user_all_video(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)

    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_all_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_all_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    return audit_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def user_pending_video(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)

    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_pending_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_pending_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    if request.method == 'POST':
        return unreg(request)
    else:
        return audit_user_pending_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def unreg(request):
    uid = request.user.id
    unreg_list = request.POST.keys()
    audit = audit_mgr.AuditMgr.instance()
    (code, res) = audit.cancel_task(uid, unreg_list)
    if code == constant.SUCCESS:
        print res
    else:
        err = 'cancel_task error.'
        print err
        return render_to_response('unreg.html', {'error':err})

    return render_to_response('unreg.html', {'unreg_list':unreg_list})

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def user_passed_video(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)

    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_passed_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_passed_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    return audit_list_page(data_list, record_count, page, pagesize, page_info)

@login_required
@permission_required("ugc.can_operate_audit_space",login_url="/forbidden/")
def user_failure_video(request):
    pagesize = PSIZE
    uid = request.user.id
    page = get_page(request)

    data_dic= get_data_dic(request)
    page_info = get_page_info(request)

    audit = audit_mgr.AuditMgr.instance()
    #(code, res) = audit.get_failure_tasklist(uid, -1, page, data_dic)
    #record_count = get_pagecount(code, res)
    (code, record_count, res) = audit.get_failure_tasklist(uid, pagesize, page, data_dic)
    data_list = get_data_list(code, res)

    return audit_list_page(data_list, record_count, page, pagesize, page_info)

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

def distribute_list_page(data_list, record_count, page_number, pagesize, start_date, end_date, tips):
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('distribute_video_count.html',
                              {'data_list': data_list,
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'end_date':end_date,
                                'start_date':start_date,
                                'tips':tips,
                                'page_count':page_count})

def search_distribute_video_page(data_list, record_count, page_number, pagesize, page_info={}):
    pytools.show_value(page_info,'page_info')

    search_list = get_search_list()
    order_list = get_order_list()
    search_key = page_info.get('search','')
    search_value = get_search_category_value(search_key)

    order_key = page_info.get('order','')
    order_value = get_order_category_value(order_key)

    page_info['search_list'] = search_list
    page_info['order_list'] = order_list

    pytools.show_value(search_value, 'search_value')
    page_info['search_value'] = search_value
    page_info['order_value'] = order_value
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    list_count = 0
    if data_list:
            list_count = len(data_list)

    return render_to_response('search_distribute_video.html',
                              {'data_list': data_list,
                                'list_count': list_count,
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'page_info': page_info,
                                'page_count':page_count})

def audit_list_page(data_list, record_count, page_number, pagesize, page_info={}):
    pytools.show_value(page_info,'page_info')

    search_list = get_search_list()
    order_list = get_order_list()
    search_key = page_info.get('search','')
    search_value = get_search_category_value(search_key)

    order_key = page_info.get('order','')
    order_value = get_order_category_value(order_key)

    page_info['search_list'] = search_list
    page_info['order_list'] = order_list

    page_info['search_value'] = search_value
    page_info['order_value'] = order_value
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('audit_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'page_info': page_info,
                                'page_count':page_count})

def get_search_category_value(key):
    if key:
        list = get_search_list()
        for k,v in list:
            if k == key:
                return v
    else:
        return ''

def get_order_category_value(key):
    if key:
        list = get_order_list()
        for k,v in list:
            if k == key:
                return v
    else:
        return ''


def admin_audit_list_page(data_list, record_count, page_number, pagesize,page_info={}):
    pytools.show_value(page_info,'page_info')
    search_list = get_search_list()
    order_list = get_order_list()
    search_key = page_info.get('search','')
    search_value = get_search_category_value(search_key)

    order_key = page_info.get('order','')
    order_value = get_order_category_value(order_key)

    page_info['search_list'] = search_list
    page_info['order_list'] = order_list

    page_info['search_value'] = search_value
    page_info['order_value'] = order_value

    
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('audit_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'admin_audit':'&edit=0',
                                'is_edit':'&edit=0',
                                'page_info': page_info,
                                'page_count':page_count})

def admin_audit_all_list_page(data_list, record_count, page_number, pagesize,page_info={}):
    pytools.show_value(page_info,'page_info')
    search_list = get_search_list()
    order_list = get_order_list()
    search_key = page_info.get('search','')
    search_value = get_search_category_value(search_key)

    order_key = page_info.get('order','')
    order_value = get_order_category_value(order_key)

    page_info['search_list'] = search_list
    page_info['order_list'] = order_list

    page_info['search_value'] = search_value
    page_info['order_value'] = order_value

    
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('audit_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'is_edit':'&edit=0',
                                'page_info': page_info,
                                'page_count':page_count})

def user_count_page(data_list, record_count, page_number, pagesize, start_date, end_date, tips):
    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)
    return render_to_response('user_count.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'end_date':end_date,
                                'start_date':start_date,
                                'tips':tips,
                                'page_count':page_count})

def audit_user_pending_list_page(data_list, record_count, page_number, pagesize, page_info={}):
    pytools.show_value(page_info,'page_info')

    search_list = get_search_list()
    order_list = get_order_list()
    search_key = page_info.get('search','')
    search_value = get_search_category_value(search_key)

    order_key = page_info.get('order','')
    order_value = get_order_category_value(order_key)

    page_info['search_list'] = search_list
    page_info['order_list'] = order_list

    page_info['search_value'] = search_value
    page_info['order_value'] = order_value

    page_range, page_count, page_number_last, page_number_next = list_info(record_count,pagesize,page_number)

    return render_to_response('audit_list.html',
                              {'data_list': data_list,
                                'list_count':len(data_list),
                                'record_count':record_count,
                                'page_number':page_number,
                                'page_count':page_count,
                                'page_number_last':page_number_last,
                                'page_number_next':page_number_next,
                                'page_range':page_range,
                                'unreg':True,
                                'page_info': page_info,
                                'page_count':page_count})

def jstest(request):
    return render_to_response('jstest.html',{})


def play_msvideo(request):
    if not request.GET.has_key("tid"):
        return render_to_response("error.html",{"title":"no tid specified"})
    tid = request.GET["tid"]
    audit = audit_mgr.AuditMgr.instance()
    url = audit.get_video_msurl(tid)
    if not url:
        return render_to_response("error.html",{"title":"invalid parameter"})
    return HttpResponseRedirect(url)
