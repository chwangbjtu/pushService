#-*- coding: utf-8 -*-
from tornado import log
import traceback
import time
import urllib 
import urllib2
import etc
import json
import sys
sys.path.append("../")

class HttpClient(object):
    def __init__(self):
        pass
        
    def get_task(self, total = 1000):
        content = None
        url_path = "/v2/service/get_task?total=" + str(total)
        url = etc.URL_TYPE + etc.PUSH_SERVER_HOST + url_path
        log.app_log.info("get task url: " + url)
        times = 0
        try:
            while times < 3:
                response = urllib2.urlopen(url)
                content = response.read()
                if content:
                    break
                
                times += 1
                    
        except Exception, e:
            log.app_log.info("get task error")
            log.app_log.info(traceback.format_exc())
           
        finally:
            return content
        
    def del_token(self, token_list):
        content = None
        url_path = "/v2/service/del_token"
        url = etc.URL_TYPE + etc.DEVICE_MANAGER_HOST + url_path
        log.app_log.info("delete token url: " + url)
        try:
            token_obj = {}
            token_obj['device_token'] = token_list
            token_json = json.dumps(token_obj)
            req = urllib2.Request(url, token_json)
            
            times = 0
            deleted = False
            while times < 3:
                response = urllib2.urlopen(req)
                content = response.read()
                ret_json = json.loads(content)
                log.app_log.info(ret_json)
                if ret_json['retcode'] == '200':
                    deleted = True
                    break
                
                times += 1
                
            if not deleted:
                raise Exception("delete tokens error")
            else:
                log.app_log.info("delete tokens success: " + token_json)
                
        except Exception, e:
            log.app_log.info("delete tokens error")
            log.app_log.info(traceback.format_exc())
        
        return content
    
    def rep_task(self, report):
        content = None
        url_path = "/v2/service/rep_task"
        url = etc.URL_TYPE + etc.PUSH_SERVER_HOST + url_path
        log.app_log.info("rep_task url: " + url)
        try:
            report_json = json.dumps(report)
            req = urllib2.Request(url, report_json)
            
            times = 0
            reported = False
            while times < 3:
                response = urllib2.urlopen(req)
                content = response.read()
                ret_json = json.loads(content)
                if ret_json['retcode'] == '200':
                    reported = True
                    break
                
                times += 1
            
            if not reported:
                raise Exception("report task error")
            else:
                log.app_log.info("report task success: " + report_json)
            
        except Exception, e:
            log.app_log.info("report task error")
            log.app_log.info(traceback.format_exc())
        
        return content
        
