#!/usr/bin/python
# -*- coding:utf-8 -*- 

# Create your views here.

import json
import urllib2

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings

from ugc.log import masterlogging
from ugc.log import logginghelper
from ugc.log import utils
from ugc.news import error
from ugc.upload import conf

def add_news(request):
    raw_body = request.body
    key_info = ""
    if request.GET.has_key("tm") and request.GET.has_key("key"):
        key_info = request.GET["tm"] + request.GET["key"]
    if not authenticate(key_info):
        return HttpResponse(error.pack_errinfo_json(error.ERROR_SYSTEM_NOT_AUTHENTICATED))
    if request.method != "POST":
        masterlogging.error(logginghelper.LogicLog("news_pusher","PushNews","fail","wrong http method"))
        return HttpResponse(error.pack_errinfo_json(error.ERROR_HTTP_METHOD_NOT_SUPPORTED))
    news_info = raw_body
    success,ret = parse_news(news_info)
    if success:
        post_task(ret)
        masterlogging.info(logginghelper.LogicLog("news_pusher","PushNews","ok","None"))
        return HttpResponse('{"result":"ok"}')
    err_code = ret
    masterlogging.info(logginghelper.LogicLog("news_pusher","PushNews","ok",err_code[1]))
    return HttpResponse(error.pack_errinfo_json(err_code))
    
def parse_news(news_json_list):
    task_list = []
    try:
        news_list = json.loads(news_json_list)["news"]
        for item in news_list:
            success,ret = format_task(item)
            if success:
                task_list.append(ret)
            else:
                return (success,ret)
        return (True,task_list)
    except Exception,e:
        masterlogging.info(logginghelper.LogicLog("news_pusher","Parse_News","exception",str(e)))
        return (False,error.ERROR_JSON_SYNTAX_ERROR)

def format_task(news_obj):
    segs = ("newsid","title","type","tags","brief","pv","time","img","video")
    for key in segs:
        if not news_obj.has_key(key):
            masterlogging.info(logginghelper.LogicLog("news_pusher","FormatTask","missing key",key))
            return (False,error.ERROR_PARAM_ARG_MISSING)
    task_obj = {}
    task_obj["uid"] = 30
    task_obj["site"] = "kkn"
    task_obj["origin"] = "push"
    task_obj["vid"] = "%s|%s" % (news_obj["newsid"],news_obj["video"])
    task_obj["title"] = news_obj["title"]
    task_obj["channel"] = u"新闻"
    task_obj["priority"] = 8
    task_obj["tags"] =  "%s|%s" % (news_obj["type"],news_obj["tags"].replace(",","|"))
    task_obj["describe"] = news_obj["brief"]
    task_obj["pub_time"] = news_obj["time"]
    return (True,task_obj)

def authenticate(key_info):
    return True

def post_task(task_list):
    try:
        for item in task_list:
            args = json.dumps(item)
            request = urllib2.Request(conf.MAZE_APPLY_TASK_URL,args)
            opener = urllib2.build_opener()
            response = opener.open(request).read()
            result = json.loads(response)
            if result["result"] == "ok":
                masterlogging.info(logginghelper.LogicLog("None","ApplyTask","ok","tid:%s"%result["tid"]))
                continue
            err_msg = result["err"]["info"]
            masterlogging.error(logginghelper.LogicLog("None","apply_task","fail",err_msg))
            return False
    except Exception,e:
        masterlogging.error(logginghelper.LogicLog("None","apply_task","exception",str(e)))
        return False
