# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import device
from tornado import log
import json

class AppRegisterV1Handler(tornado.web.RequestHandler):           
    def get(self):  
        response = {}
        try:
            deviceid = self.get_query_argument('deviceid', '')
            devicetoken = self.get_query_argument('devicetoken', '')
            os_type = self.get_query_argument('os_type', '')
            sys_ver = self.get_query_argument('sys_ver', '')
            hardware_info = self.get_query_argument('hardware_info', '')
            cli_ver = self.get_query_argument('cli_ver', '')
            
            if not deviceid or not devicetoken or not os_type or not sys_ver or not hardware_info or not cli_ver:
                raise Exception("argument error")
                
            devicetoken = ''.join(devicetoken.split())
            devicetoken = devicetoken[1 : len(devicetoken)-1]

            device_info = {}
            device_info['dt'] = devicetoken
            device_info['mac'] = deviceid
            device_info['cl'] = os_type
            device_info['ve'] = cli_ver
            device_info['os'] = sys_ver
            device_info['hardware'] = hardware_info
            
            device_mgr = device.DaoDeviceMgr()
            device_mgr.insert_device(device_info)      
            response['return'] = 'succ'
        
        except Exception, e:
            response['return'] = "error"
            response['errinfo'] = str(e)
            log.app_log.info(str(e))
        
        finally:
            self.write(json.dumps(response))
            