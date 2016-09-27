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
class LindaSender(object):
    def __init__(self, q_mgr, dst_url):
        self._db_conn = MysqlConnect()
        self._http_client = HttpClient()
        self._q_mgr = q_mgr
        self._ep_stat_dao = EpisodeStatusDao()
        self._url_selector = UrlSelector(dst_url, 'rb')
        self._handler = {}
        
    def __call__(self):
        #time_first=int(time.time())
        #time_now=int(time.time())
        #count = 0
        while True:
            try:
                send_queue = self._q_mgr.get_queue('mz_q')
                dpm = send_queue.get_dispatch_per_minute()
                if not dpm:
                    time.sleep(1)
                    continue
                elif 0==int(dpm):
                    time.sleep(Conf.linda_query_interval)
                    continue
                item = send_queue.pop_tail()
                log.app_log.warn('get item: %s' % item)
                if item:
                    data = item['data']
                    if 'retry' not in item:
                        item['retry'] = 1

                    try:
                        if item['retry'] > Conf.max_retry:
                            #send fail
                            log.app_log.warn('send fail: %s' % data['show_id'])
                            continue
                        else:
                            #send data
                            ret = self.sender_handle(data)
                            if ret['code'] == Util.RET_OK:
                                log.app_log.warn('send ok: %s' % data['show_id'])
                                #count = count+1
                                '''
                                time_now = int(time.time())
                                tmp = time.localtime(time_now)
                                hour = tmp.tm_hour
                                #max_send_num = 100
                                if hour>6 and hour <23:
                                    time.sleep(60/Conf.busy_max_send_num)
                                    #max_send_num = Conf.busy_max_send_num -1
                                else:
                                    time.sleep(60/Conf.idle_max_send_num)
                                    #max_send_num = Conf.idle_max_send_num -1
                                '''
                                time.sleep(60/int(dpm))
                                '''
                                if count > max_send_num:
                                    if time_now-time_first <60:
                                        time.sleep(60-(time_now-time_first))
                                        time_first = int(time.time())
                                        count = 0
                                    else:
                                        time_first = time_now
                                        count = 0 
                                '''
                                continue
                            elif ret['code'] == Util.RET_FAIL:
                                #retry
                                log.app_log.warn('retry: %s' % data['show_id'])
                                item['retry'] += 1
                                send_queue.add_head(item)
                                time.sleep(Conf.fail_sleep_time)
                                continue
                            elif ret['code'] == Util.RET_REJECT:
                                log.app_log.warn('reject: %s, reason: %s' % (data['show_id'], ret['msg']))
                                continue
                            elif ret['code'] == Util.RET_DROP:
                                log.app_log.warn('drop: %s' % data['show_id'])
                                continue
                            elif ret['code'] == Util.RET_ERROR:
                                log.app_log.warn('error: %s' % data['show_id'])
                                continue
                            else:
                                log.app_log.warn('send return unknown code: %s' % data['show_id'])
                    except Exception, e:
                        #send fail
                        item['retry'] += 1
                        send_queue.add_head(item)
                        time.sleep(Conf.fail_sleep_time)
                        log.app_log.warn('send get exception and retry: %s' % data['show_id'])
                        log.app_log.warn(traceback.format_exc())
            except Exception, e:
                log.app_log.error(traceback.format_exc())

            time.sleep(Conf.common_sleep_time)

    def adapt_linda_priority(self, priority):
        priority = int(priority)
        if priority >= 7:
            return '3'
        elif priority >=5:
            return '2'
        else:
            return '1'

    def generate_content(self, episode):
        try:
            for k,v in episode.items():
                if v is None:
                    episode[k] = ""
            now=int(time.time()) 
            content={"name":episode['title'],"title":episode['title'],"tags":episode['tag'],"description":episode['description'],"still":"", \
                    "creater":"564","channel":episode['category'],"language":"","category":episode['category'],"urltype":"2", \
                    "url":episode['url'],"sign":"","ori_id":str(episode["id"]),"source_type":"6","time":str(now),"inject_auto":"0","publish_system":"1"}
            #tags
            if episode['site_name']=='youtube':
                content.update({"urltype":"4"})
            if not content['tags']:
                content.update({'tags': episode['category']})
            #description
            if not content['description']:
                content.update({'description': episode['title']})
            #if content['category']==u'爱奇艺':
            if int(episode['audit']) == 0:
                content['inject_auto']='1'
            return content
        except Exception, e:
            log.app_log.error('episode content error: %s' % episode['show_id'])
            log.app_log.error(traceback.format_exc())

    def check_drop(self, episode):
        try:
            #filter_channel = [u'综艺片花', u'综艺', u'新闻', u'资讯']
            if int(episode['duration']) >3600:
                return False
            if episode['category'] == u'资讯':
                if int(episode['duration']) > 600:
                    return False
            check_duration_channel = [u'电影片花', u'电视剧片花', u'电视片花',u'综艺片花', u'动漫片花',u'电影',u'电视剧','综艺','动漫']
            if str(episode['origin']) == '0' and episode['category'] in check_duration_channel and int(episode['duration']) > 180:
                return False
            return True
        except Exception, e:
            log.app_log.error('check drop error: %s' % episode['show_id'])
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
            
            log.app_log.warn('send: %s' % content)
            con_string = json.dumps(content)
            url = self._url_selector.get_url()
            res = self._http_client.post_data(url, con_string)
            log.app_log.warn('send %s to %s' % (episode['show_id'], url))
            if res[0] == 200:
                ret_json = json.loads(res[1])
                log.app_log.warn('ret: %s' % ret_json)
                if 'result' in ret_json and ret_json["result"]=='success':
                    return {'code': Util.RET_OK}
                else:
                    return {'code': Util.RET_REJECT, 'msg': ret_json['msg']}
            return {'code': Util.RET_FAIL, 'msg': ''}
            
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return {'code': Util.RET_ERROR, 'msg': ''}

if __name__ == "__main__":
    from queue_mgr import QueueManager

    mgr = QueueManager()
    q.add_tail({'retry': 1, 'data': {'title': u'foo', 'show_id': u'XNzIzNjU0NzQ4', 'tag': u't|a|g', 'category': u'bar', 'site_code': 'youku', 'url': 'http://www.baidu.com', 'site_name': 'youku'}})
    LindaSender(mgr, Conf.add_linda_task_url, None)()
