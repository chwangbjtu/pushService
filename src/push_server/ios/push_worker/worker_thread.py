#-*- coding: utf-8 -*-
from multiprocessing import Process
from api import http_client
from tornado import log
import traceback
import etc
import json
import time
import handle_work
from statistics import Statistics
from tokens import TokenMgr

class WorkerThread(Process):
    def __init__(self):
        Process.__init__(self)
        self._client = http_client.HttpClient()
        self._handler = handle_work.HandleWork()
        self._statistics = Statistics()
        self._token_mgr = TokenMgr()
        self._token_mgr.init_data()
    
    def run(self):
        while True:
            try:
                #get task
                content = self._client.get_task(etc.TASK_NUM)
                if not content:
                    raise Exception("server error, no content return")
                    
                #parse task
                task_info = self._parse_task(content)
                if task_info:
                    task_list = task_info['tasks']
                    pull_id = task_info['pull_id']
                    msgid = task_info['msgid']
                    
                    if task_list:
                        #init statistics data
                        total = len(task_list)
                        self._statistics.init_data(total, msgid, pull_id)
                        
                        while task_list:
                            #push msg
                            task_list_item = task_list[: etc.TASK_LIST_MAX]
                            self._handler.push(task_list_item)
                            task_list = task_list[etc.TASK_LIST_MAX: ]
                        
                        #report to push manager
                        result = self._statistics.get_result()
                        self._client.rep_task(result)
                        
                        #delete invalid tokens
                        self._token_mgr.delete_token()
                
                else:
                    time.sleep(etc.ERROR_WAIT_TIME)
                
            except Exception, e:
                log.app_log.info(e)
                time.sleep(etc.ERROR_WAIT_TIME)
                continue
                
    def _parse_task(self, content):
        task_json = json.loads(content)
        if not task_json.has_key('retcode'):
            raise Exception(etc.TASK_FORMAT_ERROR)
            
        if task_json['retcode'] != '200':
            return None
            
        if not task_json.has_key('device_info') or not task_json.has_key('msg_info') or not task_json.has_key('pull_id') or not task_json.has_key('msgid'):
            raise Exception(etc.TASK_FORMAT_ERROR)
            
        device_info = task_json['device_info']         
        if not device_info.has_key('token') or not device_info.has_key('app_name'):
            raise Exception(etc.DEVICE_INFO_FORMAT_ERROR)
        
        app_name = device_info['app_name']
        msg_info = task_json['msg_info']
        msg_info_json = json.loads(msg_info)
        body = msg_info_json['content']
        msgid = task_json['msgid']

        task_list = []
        for token in device_info['token']:
            task_dict = {}
            task_dict['app_name'] = app_name
            task_dict['body'] = body
            task_dict['msgid'] = msgid
            task_dict['token'] = token
            task_list.append(task_dict)
            
        result = {}
        result['tasks'] = task_list
        result['pull_id'] = task_json['pull_id']
        result['msgid'] = msgid
        result['app_name'] = app_name
        
        log.app_log.info("get task success: " + content)
        return result

if __name__ == '__main__':
    thread = WorkerThread()
    thread.start()
    thread.join()
    