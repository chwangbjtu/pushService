# -*-coding:utf-8 -*-
import tornado.web
import sys
sys.path.append(".")
from dao import device
from tornado import log
import json

class DelDeviceHandler(tornado.web.RequestHandler):
    def post(self):
        response = {}
        response['retcode'] = 200
        response['retmsg'] = 'ok'
        
        try:
            args = self.request.body
            token_dict = json.loads(args)
            token_list = token_dict['device_token']
            
            device_mgr = device.DaoDeviceMgr()
            device_mgr.delete_tokens(token_list)
            
        except Exception, e:
            response['retcode'] = 500
            response['retmsg'] = str(e)
            log.app_log.info(str(e))
        
        finally:
            self.write(json.dumps(response))
            