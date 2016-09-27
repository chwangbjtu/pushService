# -*- coding:utf-8 -*-
import MySQLdb
from tornado import log
import traceback
import sys
sys.path.append('.')
from common.conf import Conf

class MysqlConnect(object):

    def __init__(self):
        self._db_conn = None
        self.reconnect()

    def __del__(self):
        self.close()

    def close(self):
        if self._db_conn:
            self._db_conn.close()
            self._db_conn = None

    def reconnect(self):
        try:
            self.close()
            self._db_conn = MySQLdb.connect(host=Conf.db_host, 
                                            user=Conf.db_user, 
                                            passwd=Conf.db_password, 
                                            db=Conf.db_name, 
                                            port=Conf.db_port, 
                                            charset='utf8')
            self._db_conn.autocommit(False)
        except Exception, e:
            log.app_log.error("Connect exception: %s" % traceback.format_exc())

    def commit(self):
        if self._db_conn:
            try:
                self._db_conn.commit()
                return True
            except Exception, e:
                self._db_conn.rollback()
                log.app_log.error("Commit exception: %s" % traceback.format_exc())
                return False

    def rollback(self):
        if self._db_conn:
            try:
                self._db_conn.rollback()
                return True
            except Exception, e:
                log.app_log.error("Rollback exception: %s" % traceback.format_exc())
                return False

    def execute_sql(self, sql, para=None):
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor()
                if para:
                    cursor.execute(sql, para)
                else:
                    cursor.execute(sql)
                cursor.close()
            except (AttributeError, MySQLdb.OperationalError):
                self.reconnect()
                self.execute_sql(sql, para)
            except Exception, e:
                cursor.close()
                log.app_log.error("Execute sql : %s, exception: %s" % (sql, traceback.format_exc()))

    def db_fetchall(self, sql, para=None, as_dic=False):
        if self._db_conn:
            try:
                if as_dic:
                    cursor = self._db_conn.cursor(MySQLdb.cursors.DictCursor)
                else:
                    cursor = self._db_conn.cursor()
                if para:
                    cursor.execute(sql, para)
                else:
                    cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                return result
            except (AttributeError, MySQLdb.OperationalError):
                self.reconnect()
                return self.db_fetchall(sql, para, as_dic)
            except Exception, e:
                cursor.close()
                log.app_log.error("Fetchall sql : %s, exception: %s" % (sql, traceback.format_exc()))

    def call_proc_db(self, proc_name, tuple_list):
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor()
                cursor.callproc(proc_name, tuple_list)
                row = cursor.fetchone()
                if row:
                    cursor.close()
                    self._db_conn.commit()
            except (AttributeError, MySQLdb.OperationalError):
                self.reconnect()
                self.call_proc_db(sql, proc_name, tuple_list)
            except Exception, e:
                cursor.close()
                log.app_log.error("Call proc: %s, exception: %s" % (proc_name, traceback.format_exc()))

import os
import datetime

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        if db_conn:
            show_id = 'XNzEzODc3ODI0'
            sql = "insert into episode (show_id) values (%s)"
            para = (show_id, )
            db_conn.execute_sql(sql, para)

            sql = "select episode_id, show_id from episode where show_id = %s"
            para = (show_id, )
            res = db_conn.db_fetchall(sql, para)
            print res
            for r in res:
                log.app_log.debug('get episode %s: %s' % (r[0], r[1]))

            db_conn.commit()
            db_conn.close()
    except Exception as e:
        log.app_log.error("Exception: %s" % traceback.format_exc())
