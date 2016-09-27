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
from db.episode_status_dao import EpisodeStatusDao

class MazeSender(object):
    def __init__(self, q_mgr, dst_url,dst_url_addr):
        self._db_conn = MysqlConnect()
        self._http_client = HttpClient()
        self._q_mgr = q_mgr
        self._ep_stat_dao = EpisodeStatusDao()
        self._url_selector = UrlSelector(dst_url,dst_url_addr, 'rb')
        self._handler = {}
        
    def __call__(self):
        while True:
            try:
                send_queue = self._q_mgr.get_queue('mz_q')
                item = send_queue.pop_tail()
                log.app_log.warn('get item: %s' % item)
                if item:
                    data = item['data']
                    if 'retry' not in item:
                        item['retry'] = 1

                    try:
                        if item['retry'] > Conf.max_retry:
                            #send fail
                            self._ep_stat_dao.update_send_stat(data['id'], 'FAIL')
                            log.app_log.warn('send fail: %s' % data['show_id'])
                            continue
                        else:
                            #send data
                            ret = self.sender_handle(data)
                            if ret['code'] == Util.RET_OK:
                                self._ep_stat_dao.update_send_stat(data['id'], 'OK', ret['msg'])
                                log.app_log.warn('send ok: %s' % data['show_id'])
                                #time.sleep(Conf.common_sleep_time)
                                continue
                            elif ret['code'] == Util.RET_FAIL:
                                #retry
                                log.app_log.warn('retry: %s' % data['show_id'])
                                item['retry'] += 1
                                send_queue.add_tail(item)
                                time.sleep(Conf.fail_sleep_time)
                                continue
                            elif ret['code'] == Util.RET_REJECT:
                                self._ep_stat_dao.update_send_stat(data['id'], 'REJECT')
                                log.app_log.warn('reject: %s' % data['show_id'])
                                continue
                            elif ret['code'] == Util.RET_DROP:
                                self._ep_stat_dao.update_send_stat(data['id'], 'DROP')
                                log.app_log.warn('drop: %s' % data['show_id'])
                                continue
                            elif ret['code'] == Util.RET_ERROR:
                                self._ep_stat_dao.update_send_stat(data['id'], 'ERROR')
                                log.app_log.warn('error: %s' % data['show_id'])
                                continue
                            else:
                                log.app_log.warn('send return unknown code: %s' % data['show_id'])
                    except Exception, e:
                        #send fail
                        item['retry'] += 1
                        send_queue.add_tail(item)
                        time.sleep(Conf.fail_sleep_time)
                        log.app_log.warn('send get exception and retry: %s' % data['show_id'])
            except Exception, e:
                log.app_log.error(traceback.format_exc())

            time.sleep(Conf.common_sleep_time)

    def generate_content(self, episode):
        try:
            for k,v in episode.items():
                if v is None:
                    episode[k] = ""

            #origin and uid
            origin = Conf.default_origin
            uid = Conf.default_uid
            print episode
            if str(episode['origin']) == '1':
                uid = Conf.customer_uid
                if str(episode['type']) == '1':
                    origin = 'forwards' 
                elif str(episode['type']) == '2':
                    origin = 'upload' 


            content = {'origin': origin, 'describe': episode['description'], 'uid': uid, \
                        'vid': Util.get_vid_from_url(episode['site_code'], episode['url'], episode['show_id']), 'title': episode['title'], \
                        'tags': episode['tag'], 'site': episode['site_code'], 'channel':episode['category']}        
            #tags
            if not content['tags']:
                content.update({'tags': episode['category']})
            #description
            if not content['describe']:
                content.update({'describe': episode['title']})
            #priority
            if 'priority' in episode and episode['priority']:
                content.update({'priority': episode['priority']})
            #publish time
            if 'upload_time' in episode and episode['upload_time']:
                content.update({'pub_time': episode['upload_time']})

            return content
        except Exception, e:
            log.app_log.error('episode content error: %s' % episode['show_id'])
            log.app_log.error(traceback.format_exc())

    def check_drop(self, episode):
        try:
            if str(episode['origin']) == '0':
                '''
                filter_channel = [u'新闻']
                if episode['category'] in filter_channel:
                    return False
                '''
                check_duration_channel = [u'电影片花', u'电视片花', u'综艺片花', u'动漫片花']
                if episode['category'] in check_duration_channel and int(episode['duration']) > 180:
                    return False
            return True
        except Exception, e:
            log.app_log.error('check drop error: %s' % episode['show_id'])
            log.app_log.error(traceback.format_exc())

    def check_audit(self, episode):
        try:
            if 'audit' in episode and str(episode['audit']) == '0':
                return True
            '''
            if 'category' in episode and episode['category'] == u'广场舞':
                return True
            '''
        except Exception, e:
            log.app_log.error('check audit error: %s' % episode['show_id'])
            log.app_log.error(traceback.format_exc())
    
    def sender_handle(self, episode):
        try:
            #check drop
            if not self.check_drop(episode):
                return {'code': Util.RET_DROP, 'msg': ''}

            #get content
            content = self.generate_content(episode)
            if not content:
                return {'code': Util.RET_ERROR, 'msg': ''}

            if self.check_audit(episode):
                content.update({'audit_free': 'yes'})

            log.app_log.warn('send: %s' % content)
            if Conf.enable_addr:
                if episode['category'] == u'新闻' or episode['category'] == u'热点':
                    content['site'] = 'funshion'
                    url = self._url_selector.get_url_addr('shunde')
                else:
                    url = self._url_selector.get_url()
            else:
                url = self._url_selector.get_url()
            res = self._http_client.post_data(url, json.dumps(content))
            log.app_log.warn('send %s to %s' % (episode['show_id'], url))
            if res[0] == 200:
                ret_json = json.loads(res[1])
                log.app_log.warn('ret: %s' % ret_json)
                if 'result' in ret_json and ret_json['result'] == 'ok':
                    return {'code': Util.RET_OK, 'msg': ret_json['tid']}
                else:
                    return {'code': Util.RET_REJECT, 'msg': ''}
            return {'code': Util.RET_FAIL, 'msg': ''}
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return {'code': Util.RET_ERROR, 'msg': ''}

if __name__ == "__main__":
    from queue_mgr import QueueManager

    mgr = QueueManager()
    q.add_tail({'retry': 1, 'data': {'title': u'foo', 'show_id': u'XNzIzNjU0NzQ4', 'tag': u't|a|g', 'category': u'bar', 'site_code': 'sohu', 'url': 'http://www.baidu.com', 'site_name': 'sohu'}})
    MazeSender(mgr, Conf.add_maze_task_url, None)()
