#!/usr/bin/python
# -*- coding:utf-8 -*-

import json

from django.core.cache import cache

UPLOAD_RESULT_PROCESSING = -1
UPLOAD_RESULT_FINISHED = -2
UPLOAD_RESULT_EXCEPTION = -3
UPLOAD_RESULT_ILLEGAL = -4
UPLOAD_RESULT_TOO_LARGE = -5
UPLOAD_RESULT_TO_CANCEL = -6
UPLOAD_RESULT_CANCELED = -7

MAX_LIVE_TIME = 3600*24


class StateObj(object):
    def __init__(self,state,progress,message):
        self.state = state
        self.progress = progress
        self.message = message
    
    def printf(self):
        print self.state,self.progress,self.message

def load_obj(key_id):
    json_str = cache.get(key_id)
    if not json_str:
        return None
    try:
        map_obj = json.loads(json_str)
        obj = StateObj(map_obj["state"],map_obj["progress"],map_obj["message"])
        return obj
    except Exception,e:
        return None

def save_obj(key_id,obj,to_add,live_time):
    map_obj = {"state":obj.state,"progress":obj.progress,"message":obj.message}
    json_str = json.dumps(map_obj)
    if not live_time:
        live_time = MAX_LIVE_TIME
    if to_add:
        if cache.has_key(key_id):
            return False
        cache.add(key_id,json_str,live_time)
    else:
        if not cache.has_key(key_id):
            return False
        cache.set(key_id,json_str,live_time)
    return True


def _update_obj(key_id,map_args,live_time):
    obj = load_obj(key_id)
    if not obj:
        return False
    arg_keys = ("state","progress","message")
    for key in arg_keys:
        if map_args.has_key(key):
            setattr(obj,key,map_args[key])
    return save_obj(key_id,obj,False,live_time)

def add_obj(key_id,state=None,progress=None,message=None):
    obj = StateObj(state,progress,message)
    return save_obj(key_id,obj,True,MAX_LIVE_TIME)

def update_progress(key_id,progress):
    return _update_obj(key_id,{"progress":progress},MAX_LIVE_TIME)

def get_progress(key_id):
    obj = load_obj(key_id)
    if not obj:
        return None
    return obj.progress

def update_state(key_id,state,message=None,live_time=None):
    return _update_obj(key_id,{"state":state,"message":message},live_time)

def get_state(key_id):
    obj = load_obj(key_id)
    if not obj:
        return (None,None)
    return (obj.state,obj.message)

def add_cancel(key_id):
    key_id = "%s_cancel" % key_id
    if cache.has_key(key_id):
        return False
    cache.add(key_id,0,MAX_LIVE_TIME)
    return True

def set_cancel(key_id):
    key_id = "%s_cancel" % key_id
    if not cache.has_key(key_id):
        return False;
    cache.set(key_id,1,MAX_LIVE_TIME)
    return True

def get_cancel(key_id):
    key_id = "%s_cancel" % key_id
    return cache.get(key_id)

def clear_cancel(key_id):
    key_id = "%s_cancel" % key_id
    cache.delete(key_id)

def clear(key_id):
    cache.delete(key_id)
    key_id = "%s_cancel" % key_id
    cache.delete(key_id)

def test():
    key_id = "woshidashabi"
    print "##### add_obj #####################"
    add_obj(key_id,UPLOAD_RESULT_PROCESSING,0,None)
    print load_obj(key_id).printf()
    print "##### update and get progress #####"
    update_progress(key_id,20)
    print get_progress(key_id)
    print "##### update state #########"
    update_state(key_id,UPLOAD_RESULT_TOO_LARGE,"you can't upload file whose size is over 1G")
    print get_state(key_id)

    
    

