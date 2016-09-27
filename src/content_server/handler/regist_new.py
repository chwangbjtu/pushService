# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from common.conf import Conf
from dao import device
from tornado import log
import json
import traceback
class AppRegisterHandler(tornado.web.RequestHandler):           
    def post(self):
        response = {}
        response['retcode'] = '200'
        response['retmsg'] = 'ok'
        
        try:
            args = self.request.body
            log.app_log.info(args)
            device_info = json.loads(args)
            device_mgr = device.DaoDeviceMgr()
            device_mgr.insert_device(device_info)
        
        except Exception, e:
            response['retcode'] = '404'
            response['retmsg'] = str(e)
            log.app_log.info(str(e))
            #log.app_log.info(traceback.format_exc())
        finally:
            self.write(json.dumps(response))
            
