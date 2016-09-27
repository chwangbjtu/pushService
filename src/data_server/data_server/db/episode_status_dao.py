# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from tornado import log
import traceback
import time
from common.util import Util

class EpisodeStatusDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._episode_status_tb_name = 'episode_status'

    def insert_status(self, *args, **kwargs):
        try:
            sql = "INSERT INTO %s (eid, show_id, step_id, status, url, origin, create_time, update_time) VALUES (%%s, %%s, %%s, %%s, %%s, %%s, now(), now())" % (self._episode_status_tb_name, )
            para = (kwargs['eid'], kwargs['show_id'], kwargs['step_id'], kwargs['status'], kwargs['url'], kwargs['origin'])
            self._db_conn.execute_sql(sql, para)

            sql = "SELECT LAST_INSERT_ID() from %s" % (self._episode_status_tb_name, )
            res = self._db_conn.db_fetchall(sql)
            self._db_conn.commit()
            if res:
                return str(res[0][0])

        except Exception, e:
            log.app_log.error("insert status exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

    def set_send(self, id):
        try:
            sql = "UPDATE %s SET send = 1, update_time = now() WHERE id = %%s " % (self._episode_status_tb_name, )
            para = (id, )
            #log.app_log.debug("sql: %s para: %s" % (sql, para))
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()

        except Exception, e:
            log.app_log.error("set send exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))
    
    def get_step_status(self, id):
        step_id = None
        status = None
        try:
            sql = "select step_id,status from %s where id = %%s" % (self._episode_status_tb_name)
            para = (id,)
            res = self._db_conn.db_fetchall(sql, para)
            self._db_conn.commit()
            if len(res) > 0:
                (step_id,status) = res[0]
        except Exception, e:
            log.app_log.error("Add send result exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

        return (step_id,status)

    def update_did(self,id,did):
        try:
            sql = "update %s set did = %%s, update_time = now() where id = %%s" % (self._episode_status_tb_name)
            para = [did,id,]
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("update_did exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

    def update_status(self, id, step, status, url):
        try:
            sql = "update %s set step_id = %%s, status = %%s, url = %%s, update_time = now() where id = %%s" % (self._episode_status_tb_name)
            para = [step, status, url, id]
            #log.app_log.debug("sql: %s para: %s" % (sql, para))
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("Add send result exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

    def update_download_status(self, id, status, tid=None):
        try:
            sql = "UPDATE %s SET step_id = '10', status = %%s, update_time = now() " % (self._episode_status_tb_name)
            para = [str(Util.SEND_STATUS[status]), ]

            if tid:
                sql += " , tid = %s "
                para.append(tid)

            sql += " WHERE id = %s "
            para.append(id)

            #log.app_log.debug("sql: %s para: %s" % (sql, para))

            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("Add send result exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))    

    def update_send_stat(self, id, status, tid=None):
        try:
            sql = "UPDATE %s SET step_id = '20', status = %%s, update_time = now() " % (self._episode_status_tb_name)
            para = [str(Util.SEND_STATUS[status]), ]

            if tid:
                sql += " , tid = %s "
                para.append(tid)

            sql += " WHERE id = %s "
            para.append(id)

            #log.app_log.debug("sql: %s para: %s" % (sql, para))

            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("Add send result exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))
    
if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        episodestatusdao = EpisodeStatusDao(db_conn)

        ep_stat = {'eid':'123', 'show_id': '123', 'step_id': '10', 'status': 0, 'origin': 0, 'url': 'xx'}
        last_id = episodestatusdao.insert_status(**ep_stat)
        episodestatusdao.update_status('137', '20', '3', 'dd')
        episodestatusdao.update_send_stat('142', 'REJECT', '123')

        log.app_log.error('last insert: %s' % last_id)

    except Exception,e:
        log.app_log.error(traceback.format_exc())

