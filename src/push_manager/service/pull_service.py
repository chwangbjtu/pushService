# -*-coding:utf-8 -*-
import json
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf
from common.util import create_uuid 
from common.util import PushMethod, PushType
from common.msg_manager import MsgManager
from common.token_manager import TokenManager

class PullService(object):
   
    increment = 0
    
    def __init__(self):
        self.__msg_manager = MsgManager()
        self.__token_manager = TokenManager()
        self._platform = 'ios'

    def get_task(self, pull_number):
        res = {}
        try:
            token_part = self.__msg_manager.getone_msg_token(PushMethod.Pull)
            if not token_part:
                msg = self.__msg_manager.getone_msg_waiting(PushMethod.Pull)
                if not msg:
                    log.app_log.debug('pull service: no msg to be pulled')
                    return
                if msg['msg_type'] == PushType.Test:
                    #从custom token中获取token
                    msgid = msg['msgid']
                    result = self.__msg_manager.findone_token_custom_by_msgid(msgid)
                    token = self.token_classify(result)
                    for tk in token:
                        tk['msgid'] = msg['msgid']
                        self.__msg_manager.pushone_msg_token(PushMethod.Pull, tk)
                elif msg['msg_type'] == PushType.All:
                    #从token manager中获取token
                    token = self.__token_manager.find_token_ios() 
                    if not token:
                        log.app_log.debug('pull service: no token to be assigned')
                        return
                    for tk in token:
                        tk['msgid'] = msg['msgid']
                        self.__msg_manager.pushone_msg_token(PushMethod.Pull, tk)
                else:
                    log.app_log.info('pull service: unknow msg type')
                    return
            #获取下一批token
            device = self.next_token(pull_number)
            if device:
                #获取消息详细
                msgid = device['msgid']
                del device['msgid']
                if not device['token']:
                    return
                msg = self.__msg_manager.findone_msg_history_by_msgid(msgid)
                if msg:
                    res['msgid'] = msgid
                    res['device_info'] = device
                    res['msg_info'] = msg['payload']['summary']
                    if PullService.increment >= sys.maxint:
                        PullService.increment = 0
                    else:
                        PullService.increment += 1
                    pull_id = create_uuid(PullService.increment)
                    res['pull_id'] = pull_id
        except Exception, e:
            res = {}
            log.app_log.error(traceback.format_exc())
        finally:
            return res

    def next_token(self, pull_number):
        res = {}
        try:
            msgid = ''
            app_name = ''
            tokens = [] 
            count = 0
            while count + Conf.token_basic_number <= pull_number:
                result = self.__msg_manager.popone_msg_token(PushMethod.Pull)
                if not result:
                    break
                msgid = result['msgid']
                an = result['app_name'] if 'app_name' in result else ''
                if app_name and app_name != an:
                    self.__msg_manager.pushone_msg_token(PushMethod.Pull, result)
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
                rs_token = result[rs]
                count = 0
                token = []
                for tk in rs_token:
                    try:
                        count = count + 1 
                        token.append(tk)
                        if count == Conf.token_basic_number:
                            res.append({"app_name":rs, "token":token})
                            count = 0
                            token = []
                    except Exception, e:
                        log.app_log.error(traceback.format_exc())
                #最后几个
                if token:
                    res.append({"app_name":rs, "token":token})
                    count = 0
                    token = []
        except Exception, e:
            res = []
            log.app_log.error(traceback.format_exc())
        finally:
            return res

if __name__ == '__main__':
    test = PullService()
    print test.get_task(100)
