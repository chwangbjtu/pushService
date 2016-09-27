# -*- coding:utf-8 -*-
import MySQLdb
#from tornado import log
import logging
import logging.handlers 
import traceback

import sys
import time
#sys.path.append('.')
#from common.conf import Conf
import etc

class MysqlConnect(object):

    def __init__(self):
        self._db_conn = None
        self.connect()

    def __del__(self):
        self.close()

    def ping(self):
        try:
            self._db_conn.ping()
            return True
        except Exception, e:
            return False

    def close(self):
        try:
            if self._db_conn:
                self._db_conn.close()
                self._db_conn = None
            return True
        except Exception, e:
            return False

    def connect(self):
        try:
            self._db_conn = MySQLdb.connect(host=etc.mysqlip, 
                                            user=etc.username, 
                                            passwd=etc.passworld, 
                                            db=etc.dbname, 
                                            port=etc.mysqlport, 
                                            charset='utf8')
            self._db_conn.autocommit(False)
            return True
        except Exception, e:
            return False

    def reconnect(self):
        try:
            logging.error('++reconnect db')
            while True:
                if not self.ping():
                    self.connect()
                else:
                    break
                time.sleep(1)
            logging.error('++reconnected db')
                
        except Exception, e:
            logging.error(traceback.format_exc())

    def commit(self):
        try:
            self._db_conn.commit()
            return True
        except Exception, e:
            self.rollback()
            logging.error(traceback.format_exc())
            return False

    def rollback(self):
        try:
            self._db_conn.rollback()
            return True
        except Exception, e:
            logging.error(traceback.format_exc())
            return False

    def execute_sql(self, sql, para=None):
        try:
            cursor = self._db_conn.cursor()
            if para:
                cursor.execute(sql, para)
            else:
                cursor.execute(sql)
            cursor.close()
        except (AttributeError, MySQLdb.OperationalError), e:
            logging.error("db exception: %s" % (str(e),))
            self.reconnect()
            return self.execute_sql(sql, para)
        except Exception, e:
            cursor.close()
            logging.error("Execute sql : %s, exception: %s" % (sql, traceback.format_exc()))

    def db_fetchall(self, sql, para=None, as_dic=False):
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
        except (AttributeError, MySQLdb.OperationalError), e:
            logging.error("db exception: %s" % (str(e),))
            self.reconnect()
            return self.db_fetchall(sql, para, as_dic)
        except Exception, e:
            cursor.close()
            logging.error("Fetchall sql : %s, exception: %s" % (sql, traceback.format_exc()))

    def call_proc_db(self, proc_name, tuple_list):
        try:
            cursor = self._db_conn.cursor()
            cursor.callproc(proc_name, tuple_list)
            row = cursor.fetchone()
            if row:
                cursor.close()
                self._db_conn.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            logging.error("db exception: %s" % (str(e),))
            self.reconnect()
            self.call_proc_db(proc_name, tuple_list)
        except Exception, e:
            cursor.close()
            logging.error("Call proc: %s, exception: %s" % (proc_name, traceback.format_exc()))

import os
import datetime

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        if db_conn:
            show_id = 'XNzEzODc3ODI0'
            sql = "select task_id,vid from tasktable where op = %s and status= %s and site=%s order by priority desc limit 1"
            para = ("cu","0","yk1" ,)
            res = db_conn.db_fetchall(sql, para)
            print "res",res
            if res or len(res) == 0:
                print "res is None"
            else:
                print "res is not None"
            db_conn.commit()
            db_conn.close()
            '''
            sql = "select episode_id, show_id from episode where show_id = %s"
            para = (show_id, )
            res = db_conn.db_fetchall(sql, para)
            print res
            for r in res:
                log.app_log.debug('get episode %s: %s' % (r[0], r[1]))

            db_conn.commit()
            db_conn.close()
            '''
    except Exception as e:
        #log.app_log.error("Exception: %s" % traceback.format_exc())
        logging.error("Exception: %s" % traceback.format_exc())

