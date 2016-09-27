# -*- coding:utf-8 -*-
from db_connect import MysqlConnect
from tornado import log
import traceback
from common.util import Util

class TaskDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._tb_name = 'task'

    def insert_task(self, para_dic):
        try:
            sql = "INSERT INTO %s (spider, customer, download, begin_time, end_time) VALUES (%%s, %%s, %%s, %%s, %%s)" % (self._tb_name, )
            para = (para_dic['spider'], para_dic['customer'], para_dic['download'], para_dic['begin_time'], para_dic['end_time'])
            res = self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()

        except Exception, e:
            log.app_log.error("insert_task exception: %s " % traceback.format_exc())
    
if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        task_dao = TaskDao(db_conn)

        task = {'spider': '2', 'customer': '3', 'download': '5', 'begin_time': '2014-10-1', 'end_time': '2014-12-22'}
        task_dao.insert_task(task)
        db_conn.commit()

    except Exception,e:
        log.app_log.error(traceback.format_exc())
