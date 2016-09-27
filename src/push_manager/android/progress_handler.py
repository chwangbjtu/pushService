# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.') 
from common.msg_manager import MsgManager

class ProgressHandler(object):

    def __init__(self):
        self.__msg_manager = MsgManager()

    def handle(self, para=None, body=None):
        result = ''
        try:
            ip = para['ip'] if 'ip' in para else None
            if not ip or not body:
                return result
            log.app_log.debug('progress handler: android push server(%s) report progress, content: %s' % (ip, body))  
            json_body = json.loads(body)
            msgs = json_body['result'] if 'result' in json_body else []
            right = True
            for msg in msgs: 
                msgid = msg['msgid']
                if msgid:
                    total = msg['total_conn'] if 'total_conn' in msg else 0
                    success = msg['success'] if 'success' in msg else 0
                    fail = msg['fail'] if 'fail' in msg else 0
                    msg_progress_detail = {'msgid':msgid, 'reportid':ip, 'total':total, 'success':success, 'fail':fail}
                    if self.__msg_manager.update_or_insert_msg_progress_detail(msg_progress_detail):
                        continue
                    else:
                        right = False
                        break
                else:
                    right = False
                    break
            if right:
                res = {}
                res['retcode'] = '200'
                res['retmsg'] = 'ok'
                result = json.dumps(res)
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            if not result:
                res = {}
                res['retcode'] = '404'
                res['retmsg'] = 'not found'
                result = json.dumps(res)
            return result
