# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.') 
from common.msg_manager import MsgManager

class RepTaskHandler(object):

    def __init__(self):
        self.__msg_manager = MsgManager()

    def handle(self, para=None, body=None):
        result = ''
        try:
            if not body:
                return result
            log.app_log.debug('rep task handler: ios push server report progress, content: %s' % (body,))  
            json_body = json.loads(body)
            msgid = json_body['msgid']
            pull_id = json_body['pull_id']
            if msgid and pull_id:
                total = int(json_body['total']) if 'total' in json_body else 0 
                success = int(json_body['success']) if 'success' in json_body else 0 
                fail = int(json_body['fail']) if 'fail' in json_body else 0 
                msg_progress_detail = {'msgid':msgid, 'reportid':pull_id, 'total':total, 'success':success, 'fail':fail}
                if self.__msg_manager.update_or_insert_msg_progress_detail(msg_progress_detail):
                    res = {}
                    res['retcode'] = '200'
                    res['retmsg'] = 'ok'
                    result = json.dumps(res)
                    return result
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            if not result:
                res = {}
                res['retcode'] = '404'
                res['retmsg'] = 'not found'
                result = json.dumps(res)
            return result
