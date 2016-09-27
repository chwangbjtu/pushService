# -*- coding:utf-8 -*-
from tornado import log
import time
import traceback
import json

import sys
sys.path.append('.')
from common.conf import Conf
from common.util import Util
from http.http_client import HttpClient
from common.url_selector import UrlSelector

class Sender(object):
    def __init__(self, send_queue, dst_url):
        self._http_client = HttpClient()
        self._send_queue = send_queue
        self._url_selector = UrlSelector(dst_url, 'rb')
        
    def __call__(self):
        while True:
            try:
                item = self._send_queue.pop_tail()
                if item:
                    data = item['info']
                    site = item['site']
                    retry = 1
                    if 'retry' in item:
                        retry = item['retry']
                    else:
                        item['retry'] = retry

                    if retry > Conf.max_retry:
                        #send fail
                        log.app_log.warn('send fail: [%s, %s]' % (site, data['vid']))
                        continue
                    else:
                        #send data
                        ret = self.sender_handle(site, data)
                        if ret == Util.RET_OK:
                            log.app_log.warn('send ok: [%s, %s]' % (site, data['vid']))
                            continue
                        elif ret == Util.RET_FAIL:
                            #retry
                            log.app_log.warn('retry: [%s, %s]' % (site, data['vid']))
                            item['retry'] += 1
                            self._send_queue.add_tail(item)
                            time.sleep(Conf.fail_sleep_time)
                            continue
                        elif ret == Util.RET_REJECT:
                            log.app_log.warn('reject: [%s, %s]' % (site, data['vid']))
                            continue
                        else:
                            log.app_log.warn('send return unknown code: %s' % (site, data['vid']))
            except Exception, e:
                log.app_log.error(traceback.format_exc())

            time.sleep(Conf.common_sleep_time)
    
    def sender_handle(self, site, item):
        content = {'origin': Conf.default_origin, 'describe': '', 'uid': Conf.default_uid, 'vid': item['url'], 'title': item['title'], 'tags': '', 'site': site, 'priority': Conf.default_priority, 'channel': '', 'pub_time': '', 'audit_free': 'yes'}
        if 'brief' in item:
            content['describe'] = item['brief']
        if 'tags' in item:
            content['tags'] = item['tags']
        if 'type' in item:
            content['channel'] = item['type']
        if 'pub_time' in item:
            content['pub_time'] = item['pub_time']

        url = self._url_selector.get_url()
        res = self._http_client.post_data(url, json.dumps(content))
        if res[0] == 200:
            ret_json = json.loads(res[1])
            if 'result' in ret_json and ret_json['result'] == 'ok':
                return Util.RET_OK
            else:
                return Util.RET_REJECT

        return Util.RET_FAIL


if __name__ == "__main__":
    from mem_queue import MemQueue

    q = MemQueue('q')
    q.add_tail({'site': 'brave', 'info': {'title': u'foo', 'vid': u'XNzIzNjU0NzQ4', 'url': u'http://xxx/1.mp4', 'type': u'bar', 'brief':'introo', 'tags': 'u|v|w', 'pub_time': '2014-09-26 00:12:33', 'img': ['1.jgp', '2.jpg']}})
    Sender(q, Conf.add_maze_task_url)()
