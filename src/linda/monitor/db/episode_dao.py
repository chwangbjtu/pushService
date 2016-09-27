# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from tornado import log
import traceback

class EpisodeDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn

    def get_channel(self, since='2016-4-1'):
        try:
            sql = "SELECT DISTINCT category FROM episode WHERE create_time > %s" 
            para = [since,]
            res = self._db_conn.db_fetchall(sql, para)
            self._db_conn.commit()

            if res:
                return [r[0] for r in res]
            return []
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)

    def get_site(self, since='2016-4-1'):
        try:
            sql = "select distinct s.site_name from episode as p join site as s on p.site_id = s.site_id where p.create_time > %s" 
            para = [since,]
            res = self._db_conn.db_fetchall(sql, para)
            self._db_conn.commit()

            if res:
                return [r[0] for r in res]
            return []
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)

    def get_video_count(self, channel, since):
        try:
            sql = "select s.site_name, count(p.id) as c from episode as p join site as s on p.site_id = s.site_id \
                    where p.category = %s and p.create_time > %s group by p.site_id" 
            para = [channel, since,]
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()

            if res:
                return res
            return []
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)
    
if __name__ == "__main__":

    try:
        import json
        episode_dao = EpisodeDao()
        res = episode_dao.get_video_count(u'资讯', '2016-4-1')
        if res:
            for r in res:
                print json.dumps(r)

    except Exception,e:
        log.app_log.error(traceback.format_exc())
