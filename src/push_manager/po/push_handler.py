# -*-coding:utf-8 -*-
import time
import json
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from conf import Conf
from common.msg_manager import MsgManager
from common.util import PushMethod, PushStat, PushType
from common.util import check_mongo
from po.sync_management import SyncManagement

'''
推送接口，采用接受到请求，立马返回
后端新建进程，处理取消的逻辑
解决重复推的问题：允许取消后的重复
'''
class PushHandler(object):

    def __init__(self):
        self.__msg_manager = MsgManager()
        self.__sync_management = SyncManagement()

        self._progress_interval_time = Conf.progress_interval_time
        self._progress_expire_time = Conf.progress_expire_time

    def handle(self, para=None, body=None):
        result = ''
        try:
            log.app_log.info('push handler: receive push msg from poseidon: %s' % (body,))
            body_data = json.loads(body)
            if not body_data:
                return result
            body_data['msg_type'] = para['push_type'] 
            if self.push(body_data):
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

    def push(self, data):
        res = None
        try:
            if not self.check_valid(data):
                res = False
                return
            if not check_mongo():
                res = False
                return
            #检测是否重复推送，排除掉已取消的
            msgid = data['msgid']
            if self.__msg_manager.findone_msg_history_by_msgid(msgid):
                msg_progress = self.__msg_manager.findone_msg_progress_by_msgid(msgid)
                if msg_progress and int(msg_progress['stat']) != PushStat.Canceled:
                    log.app_log.info('push handler: msgid(%s) had been pushed, and stat is not canceled' % (msgid,)) 
                    res = False
                    return res
            res = True
            #开启新进程处理
            proc_new = Process(target = self.sync_new_mana, args = (data,)) 
            proc_old = Process(target = self.sync_old_mana, args = (data,)) 
            proc_new.start()
            proc_old.start()
        except Exception, e:
            res = False
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res

    def sync_new_mana(self, data):
        data['start_time'] = int(data['start_time'])
        expire_time = int(time.time()) + self._progress_expire_time
        while int(time.time()) < expire_time: 
            try:
                if not check_mongo():
                    time.sleep(self._progress_interval_time)
                    continue
                if data['msg_type'] == 'test':
                    #将test推送的token存入token_custom中
                    token = data['token']
                    token_custom = {'msgid':data['msgid'], 'token':token}
                    #首先删除已经存在的msgid
                    self.__msg_manager.deletemany_token_custom_by_msgid(data['msgid'])
                    self.__msg_manager.insertone_token_custom(token_custom)
                    del data['token']
                #保存到消息历史队列
                #首先删除已经存在的msgid
                self.__msg_manager.deleteone_msg_history(data)
                self.__msg_manager.insertone_msg_history(data)
                #保存到等待推送队列
                #push
                #首先删除已经存在的msgid
                self.__msg_manager.deletemany_msg_waiting_by_msgid(PushMethod.Push, data['msgid'])
                self.__msg_manager.insertone_msg_waiting(PushMethod.Push, data)
                #pull
                #首先删除已经存在的msgid
                self.__msg_manager.deletemany_msg_waiting_by_msgid(PushMethod.Pull, data['msgid'])
                self.__msg_manager.insertone_msg_waiting(PushMethod.Pull, data)
                #新增进度结果队列
                progress_data = {'msgid':data['msgid'], 'stat':PushStat.Pushing}
                self.__msg_manager.update_or_insert_msg_progress(progress_data)
                break
            except Exception, e:
                time.sleep(self._progress_interval_time)
                log.app_log.error(traceback.format_exc()) 

    def sync_old_mana(self, data):
        try:
            #对接老版的management系统，不断重试，直到其数据全部同步到management的数据库中
            if not self.__sync_management.push(data):
                log.app_log.info('push handler: sync management failed, the msg to be abondoned') 
            else:
                log.app_log.info('push handler: sync management successfully') 
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 

    def check_valid(self, data):
        res = True
        try:
            msgid = data['msgid'] if 'msgid' in data else None
            if not msgid:
                log.app_log.info('push handler: push msg no msgid') 
                res = False
                return
            if data['msg_type'] == PushType.Test:
                if 'token' not in data or not data['token']:
                    log.app_log.info('push handler: push msg no token') 
                    res = False
                    return 
            start_time = data['start_time'] if 'start_time' in data else None
            if not start_time:
                data['start_time'] = int(time.time())
                #即时推送
                data['msg_level'] = 1 
            else:
                start_time = float(start_time)
                #定时推送
                data['msg_level'] = 0 
            payload = data['payload'] if 'payload' in data else None
            if not payload:
                log.app_log.info('push handler: push msg no payload') 
                res = False
                return
            summary = payload['summary'] if 'summary' in payload else None
            detail = payload['detail'] if 'detail' in payload else None
            if not summary or not detail:
                log.app_log.info('push handler: push msg payload no summary or detail') 
                res = False
                return
        except Exception, e:
            res = False
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res
