# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import device
from tornado import log
import json

class AppRegisterV2Handler(tornado.web.RequestHandler):           
    def get(self):  
        response = {}
        response['retcode'] = 200
        response['retmsg'] = 'ok'
        
        try:
            mac = self.get_query_argument('mac', '')
            dt = self.get_query_argument('dt', '')
            cl = self.get_query_argument('cl', '')
            ve = self.get_query_argument('ve', '')
            os = self.get_query_argument('os', '')
            hardware = self.get_query_argument('hardware', '')
            
            if not mac or not dt or not cl or not ve or not os or not hardware:
                raise Exception("argument error")
            
            device_info = {}
            device_info['mac'] = mac
            device_info['dt'] = dt
            device_info['cl'] = cl
            device_info['ve'] = ve
            device_info['os'] = os
            device_info['hardware'] = hardware
            
            device_mgr = device.DaoDeviceMgr()
            device_mgr.insert_device(device_info)
        
        except Exception, e:
            response['retcode'] = 404
            response['retmsg'] = str(e)
            log.app_log.info(str(e))
        
        finally:
            self.write(json.dumps(response))
            