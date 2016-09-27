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
from db.db_connect import MysqlConnect
from queue_mgr import QueuesManager
from db.episode_status_dao import EpisodeStatusDao 

class Flashget_Sender(object):
    def __init__(self, q_mgr, dst_url,dst_url_addr):
        self._db_conn = MysqlConnect()
        self._episodestatus_dao = EpisodeStatusDao(self._db_conn)
        self._http_client = HttpClient()
        self._q_mgr = q_mgr
        self._url_selector = UrlSelector(dst_url,dst_url_addr,'rb')
        self._handler = {}
        
    def __call__(self):
        while True:
            send_queue = self._q_mgr.get_queue('fg_q')
            try:
                item = send_queue.pop_tail()
                #log.app_log.warn('get item: %s' % item)
                if item:
                    data = item['data']
                    if 'retry' not in item:
                        item['retry'] = 1
                    retry = item['retry']
                    try:
                        if retry > Conf.max_retry:
                            #send fail
                            log.app_log.warn('send flashget fail: %s' % data['show_id'])
                            self._episodestatus_dao.update_download_status(data['episode_status_id'],'ERROR')
                            continue
                        else:
                            #send data
                            (ret,task_id) = self.sender_handle(data)
                            if ret == Util.RET_OK:
                                log.app_log.warn('send flashget ok: %s' % data['show_id'])
                                #self._episodestatus_dao.update_download_status(data['episode_status_id'],'OK')
                                #time.sleep(Conf.common_sleep_time)
                                continue
                            elif ret == Util.RET_FAIL:
                                #retry
                                log.app_log.warn('retry: %s' % data['show_id'])
                                item['retry'] += 1
                                send_queue.add_tail(item)
                                time.sleep(Conf.fail_sleep_time)
                                continue
                            elif ret == Util.RET_REJECT:
                                log.app_log.warn('flashget reject: %s' % data['show_id'])
                                self._episodestatus_dao.update_download_status(data['episode_status_id'],'ERROR')
                                continue
                            else:
                                log.app_log.warn('send return unknown code: %s' % data['show_id'])
                    except Exception, e:
                        #send fail
                        item['retry'] += 1
                        send_queue.add_tail(item)
                        time.sleep(Conf.fail_sleep_time)
                        log.app_log.error(traceback.format_exc())
                        log.app_log.warn('send get exception and retry: %s' % data['show_id'])
            except Exception, e:
                log.app_log.error(traceback.format_exc())

            time.sleep(Conf.common_sleep_time)

    
    def sender_handle(self, episode):
        task_id = None
        try:
            for k,v in episode.items():
                if v is None:
                    episode[k] = ""
            vid = Util.get_vid(episode)
            content = {'vid':vid, 'src_url': episode['url'], 'site': episode['site_code'],'id':episode['episode_status_id']}
            id = episode['episode_status_id']

            if 'op' not in content or not content['op']:
                content.update({'op':'cu'})

            #priority
            if 'priority' in episode and episode['priority']:
                content.update({'priority': episode['priority']})
            else:
                content.update({'priority': '1'})
            #log.app_log.warn('------%s---%s' % (episode['category'], str(type(episode['category']))))
            if Conf.enable_addr:
                if episode['category'] == u'新闻' or episode['category'] == u'热点':
                    url = self._url_selector.get_url_addr('shunde')
                else:
                    url = self._url_selector.get_url()
            else:
                url = self._url_selector.get_url()
            res = self._http_client.post_data(url, json.dumps(content))
            log.app_log.warn('send %s to %s' % (episode['show_id'], url))
            if res[0] == 200:
                ret_json = json.loads(res[1])
                if 'ret' in ret_json and ret_json['ret'] == '0' and "did" in ret_json:
                    did = ret_json["did"]
                    self._episodestatus_dao.update_did(id,did)
                    return (Util.RET_OK,task_id)
                else:
                    if 'ret' in ret_json and ret_json['ret'] == '1':
                        return (Util.RET_FAIL_BUSY,task_id)
                    return (Util.RET_REJECT,task_id)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

        return (Util.RET_FAIL,task_id)

if __name__ == "__main__":
    from mem_queue import MemQueue

    q = MemQueue('q')
    q.add_tail({'retry': 1, 'data': {'title': u'foo', 'show_id': u'XODUzODg3NzMy', 'tag': u't|a|g', 'category': u'bar', 'site_code': 'yk', 'url': 'http://www.baidu.com', 'site_name': 'youku'}})
    Flashget_Sender(q, Conf.add_flashget_task_url)()
