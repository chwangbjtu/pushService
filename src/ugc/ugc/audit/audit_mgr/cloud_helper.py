#!/usr/bin/python
# -*- coding:utf-8 -*- 
import etc
import json


#task_id -- 转码任务标识
def _create_taskid_list(task_id):
    try:
        ret_list = []
        ret_list.append(task_id)
        return ret_list
    except Exception,e:
        print 'create_tasklist error.',e
        return None


def produce_cloud_pack(task_id):
    try:
        json_ret = {}
        json_ret['pack_result_notify'] = "http://%s:%s%s" % (etc.MAZE_SERVICE_IP, etc.MAZE_SERVICE_PORT, etc.cloud_notify_loaded_info)
        task_list = _create_taskid_list(task_id)
        if task_list == None:
            return None
        json_ret['task_id'] = task_list
        return json.dumps(json_ret)
    except Exception,e:
        print 'produce_cloud_pack has except, ', e
        return None