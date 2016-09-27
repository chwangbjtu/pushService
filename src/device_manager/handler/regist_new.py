# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import device
from tornado import log
import json

class AppRegisterHandler(tornado.web.RequestHandler):           
    def post(self):
        response = {}
        response['retcode'] = 200
        response['retmsg'] = 'ok'
        
        try:
            args = self.request.body
            device_info = json.loads(args)
            device_mgr = device.DaoDeviceMgr()
            device_mgr.insert_device(device_info)
        
        except Exception, e:
            response['retcode'] = 404
            response['retmsg'] = str(e)
            log.app_log.info(str(e))
        
        finally:
            self.write(json.dumps(response))
            