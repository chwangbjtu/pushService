# -*- coding:utf-8 -*-
from tornado import log
import time
import traceback
import json
import sys
sys.path.append('.')
from common.conf import Conf
from http.http_client import HttpClient
class LindaQueryer(object):
    def __init__(self, q_mgr):
        self._q_mgr = q_mgr
        self._http_client = HttpClient()

    def __call__(self):
        log.app_log.info('start query_dispatching_num')
        while True:
            dispatch_per_minute = self._query()
            if dispatch_per_minute or dispatch_per_minute == 0:
                self._set(dispatch_per_minute)
            time.sleep(Conf.linda_query_interval)

    def _query(self):
        try:
            dispatch_per_minute = None
            code, body = self._http_client.get_data(Conf.linda_query_url)
            if code and int(code) == 200:
                print body
                data = json.loads(body)
                if data.get('result', '') == 'success':
                    dpm = data.get('dispatch_per_minute')
                    dispatch_per_minute = int(dpm)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        finally:
            return dispatch_per_minute

    def _set(self, dpm):
        try:
            log.app_log.info('set dispatch_per_minute:%s' % dpm)
            send_queue = self._q_mgr.get_queue('mz_q')
            send_queue.set_dispatch_per_minute(dpm)
        except Exception, e:
            log.app_log.error(traceback.format_exc())


if __name__ == "__main__":
    from sender.queue_mgr import QueuesManager
    mgr = QueuesManager()
    LindaQueryer(mgr)()
    
