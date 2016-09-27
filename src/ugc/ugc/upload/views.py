#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.cache import cache

import os.path
import error
from ugc.log import masterlogging
from ugc.log import logginghelper
import utils
from ugc.upload.post_logic import *

BASE_PRIORITY = 7
PRIORITY_LIST = (u"很高",u"高",u"中",u"低",u"很低")

@login_required 
@permission_required("ugc.can_operate_upload",login_url="/forbidden/")
def home_page(request):
    return render_to_response("upload/upload.html",{"priority_list":PRIORITY_LIST})

def upload_video(request):
    if not request.user.is_authenticated():
        return HttpResponse(error.pack_error(error.UPLOAD_ERROR_AUTHENTICATION))
    if not request.user.has_perm("ugc.can_operate_upload"):
        masterlogging.debug(logginghelper.LogicLog(request.user.username,"UploadFile","fail","no permission"))
        return HttpResponse(error.pack_error(error.UPLOAD_ERROR_PERMISSION))
    try:
        if request.FILES:
            return _recv_file(request,request.FILES)
        else:
            return _recv_form(request)
    except Exception,e:
        masterlogging.error(logginghelper.LogicLog(request.user.username,"ProcessForm","crash",str(e)))
        return HttpResponse(error.pack_error(error.UPLOAD_ERROR_SERVER_EXCEPTION))

def _recv_file(request,files):
    upload_file = None
    for file_key in files.keys():
        if file_key == "video_file":
            upload_file = files[file_key]
        else:
            files[file_key].close()
    if not upload_file:
        masterlogging.error(logginghelper.LogicLog(request.user.username,"RecvFile","fail","no file field"))
        return HttpResponse(error.pack_error(error.UPLOAD_ERROR_INVALID_FORM))
    else:
        file_path = upload_file.temporary_file_path()
        filename = os.path.basename(file_path)
        session_id = request.COOKIES["sessionid"]
        file_id = "%s_%s" % (session_id,filename)
        cache.add(file_id,file_path)
        upload_file.file.file.close()
        upload_file.file.close_called = True
        masterlogging.info(logginghelper.LogicLog(request.user.username,"RecvFile","ok",file_path))
        return HttpResponse('{"result":"ok","fileid":"%s"}' % filename)

def _recv_form(request):
    form_item = request.POST
    if not form_item.has_key("hidFileID"):
        masterlogging.info(logginghelper.LogicLog(request.user.username,"RecvForm","fail","no key hidFileID"))
        return rend_state(request,error.UPLOAD_ERROR_INVALID_FORM)
    file_key = form_item["hidFileID"]
    session_id = request.COOKIES["sessionid"]
    file_id = "%s_%s" % (session_id,file_key)
    file_path = cache.get(file_id)
    if not file_path:
        masterlogging.info(logginghelper.LogicLog(request.user.username,"RecvForm","fail","specified file cache not exists"))
        return rend_state(request,error.UPLOAD_ERROR_ILLEGAL_ACCESS)
    if not os.path.isfile(file_path) or not os.path.exists(file_path):
        clear(None,file_id)
        return rend_state(request,error.UPLOAD_ERROR_FILE_EXPIRED)
    if not check_form(form_item):
        masterlogging.error(logginghelper.LogicLog(request.user.username,"RecvForm","fail","fail to check form"))
        clear(file_path,file_id)
        return rend_state(request,error.UPLOAD_ERROR_INVALID_FORM)
    filename = os.path.basename(file_path)
    if not post_upload_task(request,form_item,filename):
        clear(file_path,file_id)
        return rend_state(request,error.UPLOAD_ERROR_SERVER_EXCEPTION)
    clear(None,file_id)
    return rend_state(request,error.UPLOAD_ERROR_SUCCESS)

def rend_state(request,err_code):
    if err_code == error.UPLOAD_ERROR_SUCCESS:
        masterlogging.info(logginghelper.LogicLog(request.user.username,"Upload","ok","None"))
        return render_to_response("upload/upload_callback.html",{"state":err_code})
    err_msg = error.parse_to_msg(err_code)
    masterlogging.error(logginghelper.LogicLog(request.user.username,"Upload","fail",err_msg))
    return render_to_response("upload/upload_callback.html",{"state":err_code,"err":err_msg})

def check_form(form_item):
    key_list = ("title","tags","channel","describe","priority","hidFileID")
    for input in key_list:
        if not form_item.has_key(input) or not form_item[input]:
            masterlogging.error(logginghelper.LogicLog("None","CheckForm","fail",input))
            return False
    priority = form_item["priority"]
    if not priority in PRIORITY_LIST:
        masterlogging.error(logginghelper.LogicLog("None","CheckForm","fail","priority:%s"%priority))
        return False
    return True
  
def post_upload_task(request,form_item,filename):
    import urllib
    url_args = urllib.urlencode({"filename":filename})
    file_url = "http://%s/upload/download/?%s" % (request.get_host(),url_args)
    args = normalize(form_item,file_url,request.user.id)
    tid = apply_task(args)
    actionid = request.COOKIES["sessionid"] + "_" + request.user.username
    if not tid:
        masterlogging.error(logginghelper.LogicLog(actionid,"apply_task","fail","None"))
        return False
#   report_state(tid,1)
    return True

def normalize(form_item,filename,uid):
    args = {"uid":uid,"site":"funshion","origin":"upload","vid":filename}
    keys = ["title","channel","tags","describe", "audit_free"]
    for key_item in keys:
        args[key_item] = form_item[key_item]
    priority_txt = form_item["priority"]
    priority = BASE_PRIORITY
    for i in range(0,len(PRIORITY_LIST)):
        if PRIORITY_LIST[i] == priority_txt:
            priority -= i
            break
    args["priority"] = priority
    return args

def finish_upload(request):
    return render_to_response("upload/finish_upload.html")

def remove_file(file_path):
    try:
        os.remove(file_path)
    except Exception,e:
        masterlogging.error(logginghelper.SystemLog(utils.get_cur_info_within_exception(),"os.remove",str(e)))


def clear(file_path,cache_key):
    if file_path:
        remove_file(file_path)
    try:
        cache.delete(cache_key)
    except Exception,e:
        pass
