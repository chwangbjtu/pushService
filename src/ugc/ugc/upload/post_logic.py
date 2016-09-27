#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
from conf import *
import urllib2
from ugc.log import masterlogging
from ugc.log import logginghelper

def apply_task(info_map):
    try:
        args = json.dumps(info_map)
        request = urllib2.Request(MAZE_APPLY_TASK_URL,args)
        opener = urllib2.build_opener()
        response = opener.open(request).read()
        result = json.loads(response)
        if result["result"] == "ok":
            return result["tid"]
        err_msg = result["err"]["info"]
        masterlogging.error(logginghelper.LogicLog("None","apply_task","fail",err_msg))
        return None
    except Exception,e:
        masterlogging.error(logginghelper.LogicLog("None","apply_task","exception",str(e)))
        return None

#def post_task(info_map):
#    try:
#        args = json.dumps(info_map)
#        request = urllib2.Request(VIPER_ADD_TASK_URL,args)
#        opener = urllib2.build_opener()
#        response = opener.open(request).read()
#        result = json.loads(response)
#        if result["result"] == "ok":
#            return True
#    except Exception,e:
#        print e
#    return False

def report_state(tid,state):
    message = '{"tid":"%s","step":"upload","status":%d}' % (tid,state)
    try:
        request = urllib2.Request(MAZE_REPORT_TASK_URL,message)
        opener = urllib2.build_opener()
        response = opener.open(request).read()
        result = json.loads(response)
        if result["result"] == "ok":
            return True
    except Exception,e:
        print e
    return False

