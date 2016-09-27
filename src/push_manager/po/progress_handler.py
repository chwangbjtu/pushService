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
            msgid = para['msgid'] if 'msgid' in para else None
            if not msgid:
                log.app_log.info('progress handler: poseidon progress argument invalid: msgid is none') 
                return result
            progress = self.progress(msgid)
            if progress:
                res = progress
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

    def progress(self, msgid):
        res = {}
        try:
            res = self.__msg_manager.getone_msg_progress_by_msgid(msgid)
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res
