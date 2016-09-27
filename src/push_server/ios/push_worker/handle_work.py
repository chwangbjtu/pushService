#-*- coding: utf-8 -*-
from apnslib.notification import *
from apnslib.notify_mgr import *
from tornado import log
import traceback
import etc
from statistics import Statistics
from tokens import TokenMgr

class HandleWork(object):
    def __init__(self):
        self._cert_objs = {}
        for cert in etc.CERT_LIST:
            self._cert_objs[cert] = APNSNotificationWrapper(cert, False)
    
    def add_failed_num(self):
        statistics_obj = Statistics()
        statistics_obj.add_failed_num()        
        
    def push(self, task_list):
        try:
            for task in task_list:
                try:
                    devicetoken = task["token"].encode("utf-8")
                    body = task["body"]
                    msgid = task["msgid"].encode("utf-8")
                    app_name = task["app_name"].encode("utf-8")
                    if not app_name in etc.CERT_LIST:
                        raise Exception("app name is invalid: " + app_name)

                    if len(devicetoken) != 64:
                        token_mgr = TokenMgr()
                        token_mgr.add_delete_token(devicetoken)
                        raise Exception("token length is invalid: " + devicetoken)
                    
                    message = APNSNotification()
                    message.token_hex(devicetoken) 
                    if body:
                        alert_l = APNSAlert()
                        alert_l.set_body(body)
                        if msgid:
                            alert_l.set_action_loc_key('play')				
                        message.alert(alert_l)
                        
                    if msgid:
                        data = {}
                        data['msgID'] = msgid
                        property = APNSProperty("customdata", data)
                        message.append_property(property)
                        
                    self._cert_objs[app_name].append(message)
                    
                except Exception, e:
                    self.add_failed_num()
                    log.app_log.info(e)
                    continue

            for cert, obj in self._cert_objs.items():
                if obj.count() != 0:
                    log.app_log.info("cert is " + cert + ", count = " + str(obj.count()))
                    self._cert_objs[cert].notify()
                
        except Exception, e:                 
                log.app_log.info(traceback.format_exc())
        
        finally:
            for cert, obj in self._cert_objs.items():
                self._cert_objs[cert].clear()
            
def __test1():    
    _statistics = Statistics()
    _statistics.init_data(2, 'lalala', 'nimeia')
    
    _token_mgr = TokenMgr()
    _token_mgr.init_data()
    
    task_item = []
    _TC1 = {}
    _TC2 = {}
    _TC1['token'] = "f42b0dec5ceb8ab71aeba3cd42a3f14dd5863436cd53dc6ddfe1a609dbc9430c"
    _TC1['app_name'] = "iphoneplayerplus"
    _TC1['body'] = "大家好"
    _TC1['msgid'] = "444"
    _TC1['expire_time'] = 0
    
    _TC2['token'] = "1111111111111111111111111111111111111111111111111111111111111111"
    _TC2['app_name'] = "iphoneplayerplus"
    _TC2['body'] = "你好"
    _TC2['msgid'] = "333"
    _TC2['expire_time'] = 0
    
    task_item.append(_TC1)
    task_item.append(_TC2)
    
    handle_work = HandleWork()
    handle_work.push(task_item)
    ret = _statistics.get_result()
    print ret
          
if __name__ == "__main__":
    import os
    __test1()
    #os.system("PAUSE")
    os.system("read -n1 -p \"Press any key to continue...\"")
    
        
