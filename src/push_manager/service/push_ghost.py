# -*-coding:utf-8 -*-
import time
import json
import traceback
from tornado import log
from multiprocessing import Process

import sys
sys.path.append('.')
from conf import Conf
from common.util import NodeType
from common.http_client import HttpClient
from common.node_manager import NodeManager
from service.push_service import PushService

'''
单独进程，循环不断地扫描push表，获取符合条件的推送消息
'''
class PushGhost(Process):
    
    def __init__(self, interval=Conf.progress_interval_time):
        Process.__init__(self)
        self._push_path = '/push_msg'

        self._progress_interval_time = interval
        self._progress_expire_time = Conf.progress_expire_time

        self.__http_client = HttpClient()
        self.__node_manager = NodeManager()
        self.__push_service = PushService()

    #call start to be run
    def run(self):
        while True:
            try:
                if not self.is_sleeping_time():
                    task = self.__push_service.get_task()
                    if task:
                        self.push_task(task)
            except Exception, e:
                log.app_log.error(traceback.format_exc())
            finally:
                time.sleep(self._progress_interval_time)

    def push_task(self, data):
        try:
            msgid = data['msgid']
            start_time = data['start_time']
            retry_times = 0
            has_push_server = True
            push_server = self.get_push_server()
            if not push_server:
                has_push_server = False
            expire_time = start_time + self._progress_expire_time
            while int(time.time()) < expire_time and not self.is_sleeping_time(): 
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
                        response = self.__http_client.post_data(url=url, body=json.dumps(data))
                        response = response['data'] if 'data' in response else response
                        log.app_log.debug('push ghost: msgid(%s) push to server(%s) response:%s' % (msgid, url, response)) 
                        if not response:
                            log.app_log.debug('push ghost: msgid(%s) push to server(%s) failed: need retry' % (msgid, url)) 
                        else:
                            #已经通知到，无需再通知
                            del push_server[i]
                            response = json.loads(response)
                            if 'retcode' in response and str(response['retcode']) == '200':
                                log.app_log.debug('push ghost: msgid(%s) push to server(%s) successfully' % (msgid, url)) 
                            else:
                                log.app_log.debug('push ghost: msgid(%s) push to server(%s) failed: no need retry' % (msgid, url)) 
                    retry_times = retry_times + 1
                    log.app_log.info('push ghost: msgid(%s) push to push server(%s retry times)' % (msgid, retry_times))
                    time.sleep(self._progress_interval_time)
                except Exception, e:
                    time.sleep(self._progress_interval_time)
                    log.app_log.error(traceback.format_exc()) 
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
            
    def is_sleeping_time(self):
        current = time.localtime(time.time())
        hour = current.tm_hour
        if (hour >= 0 and hour <= 8) or (hour >= 23 and hour <= 24):
            log.app_log.debug('current time is sleeping time, wait......')
            return True
        return False
    

if __name__ == '__main__':
    test = PushGhost()
    test.start()
