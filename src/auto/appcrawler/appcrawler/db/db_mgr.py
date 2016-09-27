# -*- coding:utf-8 -*-
import traceback
import logging
from mysql_connect import MysqlConnect
from multiprocessing import Lock
from site_dao import SiteDao
from episode_dao import EpisodeDao
from mp_channel_dao import MpChannelDao

def create_instance():
    with DbManager._lock:
        instance = DbManager()
        instance._db_conn = MysqlConnect()
        instance._daos.update({
                                'episode': EpisodeDao(instance._db_conn), 
                                'site': SiteDao(instance._db_conn),
                                'mpchannel': MpChannelDao(instance._db_conn),
                              })
        return instance

class DbManager(object):

    _db_conn = None
    _daos = {}
    _lock = Lock()

    @staticmethod
    def instance():
        with DbManager._lock:
            if not hasattr(DbManager, "_instance"):
                DbManager._instance = DbManager()
                DbManager._db_conn = MysqlConnect()
                DbManager._daos.update({
                                        'episode': EpisodeDao(DbManager._db_conn),
                                        'site': SiteDao(DbManager._db_conn),
                                        'mpchannel': MpChannelDao(DbManager._db_conn),
                                       })
            return DbManager._instance

    def commit_transaction(self):
        self._db_conn.commit()

    def insert_episode(self, item):
        try:
            dao = self._daos['episode']
            value_dict = {}

            cont_id = item['cont_id']
            site_id = item['site_id']

            value_dict['cont_id'] = cont_id
            value_dict['site_id'] = site_id

            if 'title' in item:
                value_dict['title'] = item['title']
            if 'url' in item:
                value_dict['url'] = item['url']
            if 'thumb_url' in item:
                value_dict['thumb_url'] = item['thumb_url']
            if 'duration' in item:
                value_dict['duration'] = item['duration']
            if 'cp_name' in item:
                value_dict['cp_name'] = item['cp_name']
            if 'tag' in item:
                value_dict['tag'] = item['tag']
            if 'played' in item:
                value_dict['played'] = item['played']
            if 'utime' in item:
                value_dict['utime'] = item['utime']
            if 'channel_name' in item:
                value_dict['channel_name'] = item['channel_name']
            if 'priority' in item:
                value_dict['priority'] = item['priority']

            res = dao.get_episode(cont_id, site_id)
            if not res:
                dao.insert_episode(value_dict)
            else:
                dao.update_episode(cont_id, site_id, value_dict)

            self.commit_transaction()

        except Exception,e:
            logging.log(logging.ERROR, traceback.format_exc())

    def get_site_id_by_code(self, site_code):
        try:
            dao = self._daos['site']
            res = dao.get_site_id_by_code(site_code)
            self.commit_transaction()
            return res
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def get_miaopai_task(self):
        try:
            dao = self._daos['mpchannel']
            res = dao.get_miaopai_task()
            self.commit_transaction()
            return res
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())


