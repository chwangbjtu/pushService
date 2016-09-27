# -*- coding:utf-8 -*-
from tornado import log
from datetime import datetime
import time
import traceback
import json
import sys
sys.path.append(".")
from common.conf import Conf
from common.black_filter import BlackFilter
from common.util import Util
from db.db_connect import MysqlConnect
from db.task_dao import TaskDao
from db.episode_dao import EpisodeDao
from db.episode_status_dao import EpisodeStatusDao
from db.step_dao import StepDao
import threading

class BaseService(object):
    def __init__(self, q_mgr, service_pipe):
        self._db_conn = MysqlConnect()
        self._task_dao = TaskDao(self._db_conn)
        self._ep_dao = EpisodeDao(self._db_conn)
        self._ep_stat_dao = EpisodeStatusDao(self._db_conn)
        self._step_dao = StepDao(self._db_conn)
        self._q_mgr = q_mgr
        self._service_pipe = service_pipe

        #load keyword black list
        log.app_log.debug("loading black list, wait a moment ...")
        if Conf.enable_blacklist:
            self._ep_filter = BlackFilter()
            self._ep_filter.load_blacklist()
        else:
            self._ep_filter = None

        #get steps dic
        self._step_dic = self._step_dao.get_step_dic()

    def __recv_op(self, pipe):
        try:
            if pipe.poll():
                r = pipe.recv()
                return r
        except Exception as e:
            log.app_log.error(traceback.format_exc())

    def __communicate(self, epf, pipe):
        while True:
            r = self.__recv_op(pipe)
            if r:
                res = {}
                if not epf:
                    res = {'ret': '0', 'msg': 'black filter disabled'}
                else:
                    cmd = json.loads(r)
                    if cmd['op'] == 'reload':
                        epf.reload_blacklist()
                        res = {'ret': '0'}
                    elif cmd['op'] == 'add':
                        if epf.add_black_word(cmd['content']):
                            res = {'ret': '0'}
                        else: 
                            res = {'ret': '1'}
                    elif cmd['op'] == 'filter':
                        r = epf.filt_word(cmd['content'])
                        res = {'ret': '0'}
                        res["msg"] = "filtered" if r else "passed"
                #return result
                pipe.send(json.dumps(res))
                    
            time.sleep(1)

    def __call__(self):
        try:
            t = threading.Thread(target=self.__communicate, args=(self._ep_filter, self._service_pipe))
            t.start()
            self._loop()
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def _check_episode_since(self, since):
        since_time = Util.get_now_time(delta=since)

        #get spider episode
        episodes = self._ep_dao.get_recent_episodes(since_time, stash=0, origin=0)

        spider_data = 0
        for ep in episodes:
            self._q_mgr.get_queue('ep_q').add_tail({'data': ep, 'origin': 0})
            self._ep_dao.set_send(ep['id'], origin=0)
            spider_data += 1

        #get customer episode
        episodes = self._ep_dao.get_recent_episodes(since_time, stash=0, origin=1)
        customer_data = 0
        for ep in episodes:
            self._q_mgr.get_queue('ep_q').add_tail({'data': ep, 'origin': 1})
            self._ep_dao.set_send(ep['id'], origin=1)
            customer_data += 1

        return (spider_data, customer_data)

    def _check_status_since(self, since):
        since_time = Util.get_now_time(delta=since)

        #get spider episode
        episodes = self._ep_dao.get_maze_episodes(since_time, origin=0)

        data_count = 0
        for ep in episodes:
            self._q_mgr.get_queue('mz_q').add_tail({'data': ep})
            self._ep_stat_dao.set_send(ep['id'])
            data_count += 1

        #get customer episode
        episodes = self._ep_dao.get_maze_episodes(since_time, origin=1)
        for ep in episodes:
            self._q_mgr.get_queue('mz_q').add_tail({'data': ep})
            self._ep_stat_dao.set_send(ep['id'])
            data_count += 1

        return data_count

    def _filt_episode(self, data):
        for v in data.values(): 
            if self._ep_filter and self._ep_filter.filt_word(unicode(v)):
                return True     
        return False  

    def _loop(self):
        while True:
            try:
                begin_time = Util.get_now_time()

                #push episode from ep_q to fg_q
                ep_q = self._q_mgr.get_queue('ep_q')
                fg_q = self._q_mgr.get_queue('fg_q')
                while ep_q.size() > 0:
                    data = ep_q.pop_head()
                    episode, origin = (data['data'], data['origin'])

                    #filter data if not forced
                    if ('force' not in episode or str(episode['force']) == '0') and self._filt_episode(episode):
                        log.app_log.warn('filter data: %s' % episode['show_id'])
                        ep_stat = {'eid': episode['id'], 'show_id': episode['show_id'], 'step_id': self._step_dic['send'], 'status': 3, 'url': '', 'origin': origin}
                        episode_status_id = self._ep_stat_dao.insert_status(**ep_stat)
                        continue

                    if origin == 1 and ('type' in episode and str(episode['type']) == '2'): #it means that customer uploaded episode do not need download
                        ep_stat = {'eid': episode['id'], 'show_id': episode['show_id'], 'step_id': self._step_dic['download'], 'status': 1, 'url': episode['url'], 'origin': origin}
                        self._ep_stat_dao.insert_status(**ep_stat)
                    else:
                        ep_stat = {'eid': episode['id'], 'show_id': episode['show_id'], 'step_id': self._step_dic['download'], 'status': 0, 'url': '', 'origin': origin}
                        episode_status_id = self._ep_stat_dao.insert_status(**ep_stat)

                        #send to download
                        episode['episode_status_id'] = episode_status_id
                        fg_q.add_tail({'data': episode})

                #pull new episode from db to ep_q
                (spider_data, customer_data) = self._check_episode_since(Conf.check_new_since)
                log.app_log.debug("spider episode: %s, customer episode: %s" % (spider_data, customer_data))

                #pull downloaded episode from db to mz_q
                download_count = self._check_status_since(Conf.check_status_since)
                log.app_log.debug("download episode: %s" % download_count)

                self._task_dao.insert_task({'spider': spider_data, 'customer': customer_data, 'download':download_count, 'begin_time': begin_time, 'end_time': Util.get_now_time()})

            except Exception, e:
                    log.app_log.error(traceback.format_exc())

            time.sleep(Conf.service_interval)

if __name__ == "__main__":
    from sender.queue_mgr import QueuesManager
    mgr = QueuesManager.get_instance()
    BaseService(mgr)()
