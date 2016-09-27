# -*-coding:utf-8 -*-
import time
import json
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from conf import Conf
from common.util import PushMethod, PushStat, NodeType
from common.util import check_mongo
from common.http_client import HttpClient
from common.msg_manager import MsgManager
from common.node_manager import NodeManager
from po.sync_management import SyncManagement

'''
取消接口，采用接受到请求，立马返回
后端新建进程，处理取消的逻辑
'''
class CancelHandler(object):

    def __init__(self):
        self._push_path = '/cancel_msg'

        self.__http_client = HttpClient()
        self.__node_manager = NodeManager()
        self.__msg_manager = MsgManager()
        self.__sync_management = SyncManagement()

        self._progress_interval_time = Conf.progress_interval_time
        self._progress_expire_time = Conf.progress_expire_time

    def handle(self, para=None, body=None):
        result = ''
        try:
            msgid = para['msgid'] if 'msgid' in para else ''
            if not msgid:
                log.app_log.info('cancel handler: poseidon cancel argument invalid: msgid is none')
                return result
            if self.cancel(msgid):
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

    def cancel(self, msgid):
        res = None
        try:
            res = True
            #开启新进程处理
            proc_new = Process(target = self.sync_new_mana, args = (msgid,)) 
            proc_old = Process(target = self.sync_old_mana, args = (msgid,)) 
            proc_push = Process(target = self.sync_push_server, args = (msgid,)) 
            proc_new.start()
            proc_old.start()
            proc_push.start()
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 
        finally:
            return res

    #（1）正在推送：删除
    #（2）等待推送队列：删除
    #（3）推送进度队列：更新推送状态
    def sync_new_mana(self, msgid):
        expire_time = int(time.time()) + self._progress_expire_time
        while int(time.time()) < expire_time: 
            try:
                if not check_mongo():
                    time.sleep(self._progress_interval_time)
                    continue
                #正在推送
                #push
                self.__msg_manager.deletemany_msg_token(PushMethod.Push, msgid)
                #pull
                self.__msg_manager.deletemany_msg_token(PushMethod.Pull, msgid)
                #等待推送队列
                #push
                self.__msg_manager.deletemany_msg_waiting_by_msgid(PushMethod.Push, msgid)
                #pull
                self.__msg_manager.deletemany_msg_waiting_by_msgid(PushMethod.Pull, msgid)
                #取消推送后，将token_custom清空，以免影响后续的数据(若取消后，再次以同样的msgid推送，但是token又不一样)
                self.__msg_manager.deletemany_token_custom_by_msgid(msgid)
                #推送进度队列
                msg_progress = {'msgid':msgid, 'stat':PushStat.Canceled}
                self.__msg_manager.update_or_insert_msg_progress(msg_progress)
                #取消推送后，将进度详情队列清空，以免影响后续的数据(若取消后，再次以同样的msgid推送)
                self.__msg_manager.deletemany_msg_progress_detail_by_msgid(msgid)
                break
            except Exception, e:
                log.app_log.error(traceback.format_exc()) 
                time.sleep(self._progress_interval_time)

    def sync_push_server(self, msgid): 
        try:
            #通知所有的android push server，取消推送
            retry_times = 0
            has_push_server = True
            push_server = self.get_push_server()
            if not push_server:
                has_push_server = False
            expire_time = int(time.time()) + self._progress_expire_time
            while int(time.time()) < expire_time: 
                try:
                    if not has_push_server:
                        push_server = self.get_push_server()
                        if push_server:
                            has_push_server = True
                    ps_num = len(push_server)
                    if has_push_server and ps_num <= 0:
                        break
                    connect_timeout = True
                    #倒序遍历
                    for i in range(len(push_server)-1, -1, -1):
                        url = push_server[i]
                        url = '%s%s%s' % (url, '?msgid=', msgid)
                        response = self.__http_client.get_data(url=url)
                        response = response['data'] if 'data' in response else response
                        log.app_log.debug('cancel handler: msgid(%s) cancel send to server(%s) response:%s' % (msgid, url, response)) 
                        if not response:
                            log.app_log.debug('cancel handler: msgid(%s) cancel send to server(%s) failed: need retry' % (msgid, url)) 
                        else:
                            #已经通知到，无需再通知
                            del push_server[i]
                            connect_timeout = False
                            response = json.loads(response)
                            if 'retcode' in response and str(response['retcode']) == '200':
                                log.app_log.debug('cancel handler: msgid(%s) cancel send to server(%s) successfully' % (msgid, url)) 
                            else:
                                log.app_log.debug('cancel handler: msgid(%s) cancel send to server(%s) failed: no need retry' % (msgid, url)) 
                    retry_times = retry_times + 1
                    log.app_log.info('cancel handler: msgid(%s) cancel send to push server(%s retry times)' % (msgid, retry_times))
                    time.sleep(self._progress_interval_time)
                except Exception, e:
                    time.sleep(self._progress_interval_time)
                    log.app_log.error(traceback.format_exc()) 
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 

    def sync_old_mana(self, msgid):
        try:
            #对接老版的management系统，不断重试，直到其数据全部同步到management的数据库中
            if not self.__sync_management.cancel(msgid):
                log.app_log.info('cancel handler: sync management failed, the msg to be abondoned') 
            else:
                log.app_log.info('cancel handler: sync management successfully') 
        except Exception, e:
            log.app_log.error(traceback.format_exc()) 

    def get_push_server(self):
        res = []
        try:
            nodes = self.__node_manager.findmany_node(type=NodeType.Push)
            for node in nodes:
                ip = node['ip']
                url = 'http://%s:%s%s' % (ip, Conf.push_server_port, self._push_path)
                res.append(url)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return res
