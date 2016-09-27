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
        self._tb_name = "episode"
        self._origin_tb_name = "customer_episode"

    def get_nourl_record_by_site(self, site_id, origin=0):
        try:
            tb_name = self._tb_name
            if int(origin) == 1:
                tb_name = self._origin_tb_name
            sql = "select e.show_id, e.url, e.thumb_url, e.has_img from %s as e where e.site_id=%%s and e.has_img=0" % (tb_name,)
            para = (site_id,)
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            return res
        except Exception, e:
            log.app_log.error("get undownload record by site exception: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s   para:%s" %(sql, para))

    def get_undownload_record_by_site(self, site_id, origin=0):
        try:
            tb_name = self._tb_name
            if int(origin) == 1:
                tb_name = self._origin_tb_name
            sql = "select e.show_id, e.url, e.thumb_url, e.has_img from %s as e where e.site_id=%%s and e.has_img=1" % (tb_name,)
            para = (site_id,)
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            return res
        except Exception, e:
            log.app_log.error("get undownload record by site exception: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s   para:%s" %(sql, para))

    def get_record_by_site(self, site_id, origin=0):
        try:
            tb_name = self._tb_name
            if int(origin) == 1:
                tb_name = self._origin_tb_name
            sql = "select e.show_id, e.url, e.thumb_url, e.has_img from %s as e where e.site_id=%%s and e.has_img!=2" % (tb_name,)
            para = (site_id,)
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            return res
        except Exception, e:
            log.app_log.error("get record by site exception: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s   para:%s" %(sql, para))

    def update_thumb_url(self, showid, thumb_url, has_img, origin=0):
        try:
            tb_name = self._tb_name
            if int(origin) == 1:
                tb_name = self._origin_tb_name
            sql = "update %s as e set e.thumb_url=%%s, e.has_img=%%s where e.show_id=%%s" % (tb_name,)
            para = (thumb_url, has_img, showid)
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("update episode thumb url exception: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s   para:%s" %(sql, para))
   
    def close(self):
        if self._db_conn:
            self._db_conn.close()

if __name__ == "__main__":
    try:
        db_conn = MysqlConnect()
        episode_dao = EpisodeDao(db_conn)

        res = episode_dao.get_record_by_site(site_id=1)
        if res:
            for r in res:
                log.app_log.debug(' '.join(['%s: %s' % (k, v ) for k, v in r.items()]))
    except Exception,e:
        log.app_log.error(traceback.format_exc())
