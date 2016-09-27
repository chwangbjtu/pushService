# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from common.util import PushMethod, PushType
from common.msg_manager import MsgManager
from common.token_manager import TokenManager

class PushService(object):
    
    def __init__(self):
        self.__msg_manager = MsgManager()
        self.__token_manager = TokenManager()
        self._platform = 'android'

    def get_task(self):
        res = {}
        try:
            token_part = self.__msg_manager.getone_msg_token(PushMethod.Push)
            if not token_part:
                msg = self.__msg_manager.getone_msg_waiting(PushMethod.Push)
                if not msg:
                    log.app_log.debug('push service: no msg to be pushed')
                    return
                if msg['msg_type'] == PushType.Test:
                    msgid = msg['msgid']
                    result = self.__msg_manager.findone_token_custom_by_msgid(msgid)
                    token = self.token_classify(result)
                    for tk in token:
                        tk['msgid'] = msg['msgid']
                        self.__msg_manager.pushone_msg_token(PushMethod.Push, tk)
                elif msg['msg_type'] == PushType.All:
                    #从token manager中获取token
                    tk = {'msgid':msg['msgid']}
                    self.__msg_manager.pushone_msg_token(PushMethod.Push, tk)
                else:
                    log.app_log.info('push service: unknow msg type')
                    return
            #获取下一批token
            device = self.next_token()
            if device:
                #获取消息详细
                msgid = device['msgid']
                del device['msgid']
                msg = self.__msg_manager.findone_msg_history_by_msgid(msgid)
                if msg:
                    res['msgid'] = msgid
                    res['msg_type'] = msg['msg_type']
                    res['start_time'] = msg['start_time']
                    if device['token']: 
                        res['device_info'] = device
                    res['msg_info'] = msg['payload']['detail']
        except Exception, e:
            res = {}
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def next_token(self):
        res = {}
        try:
            msgid = ''
            app_name = ''
            tokens = []
            count = 0
            while True:
                result = self.__msg_manager.popone_msg_token(PushMethod.Push)
                if not result:
                    break
                msgid = result['msgid']
                an = result['app_name'] if 'app_name' in result else ''
                if app_name and app_name != an:
                    self.__msg_manager.pushone_msg_token(PushMethod.Push, result)
                    break
                app_name = an
                token = result['token'] if 'token' in result else []
                if token:
                    count = count + len(token)
                    tokens = tokens + token
            if msgid:
                res = {'msgid':msgid, 'app_name':app_name, 'token':tokens}
        except Exception, e:
            res = {}
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def token_classify(self, token_custom):
        res = []
        try:
            token = token_custom['token'] if 'token' in token_custom else []
            result = {}
            for tk in token:
                try:
                    platform = tk['platform'] if 'platform' in tk else None
                    if platform == self._platform:
                        app_name = tk['app_name']
                        token_lst = result[app_name] if app_name in result else []
                        token_lst.append(tk['id'])
                        result[app_name] = token_lst
                except Exception, e:
                    log.app_log.error(traceback.format_exc())
            for rs in result:
                try:
                    rs_token = result[rs]
                    res.append({"app_name":rs, "token":rs_token})
                except Exception, e:
                    log.app_log.error(traceback.format_exc())
        except Exception, e:
            res = []
            log.app_log.error(traceback.format_exc())
        finally:
            return res

if __name__ == '__main__':
    test = PushService()
    print test.get_task()
