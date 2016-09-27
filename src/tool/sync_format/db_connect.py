# -*- coding:utf-8 -*-
import MySQLdb
import logging
import traceback

import sys
import time

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
            self._db_conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='funshion', db='ch_old', port=3306, charset='utf8')
            self._db_conn.autocommit(False)
            return True
        except:
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
            logging.error(traceback.format_exc())
            self.reconnect()
            self.execute_sql(sql, para)
        except Exception, e:
            cursor.close()
            logging.error(traceback.format_exc())

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
            logging.error(traceback.format_exc())
            self.reconnect()
            return self.db_fetchall(sql, para, as_dic)
        except Exception, e:
            cursor.close()
            logging.error(traceback.format_exc())

    def call_proc_db(self, proc_name, tuple_list):
        try:
            cursor = self._db_conn.cursor()
            cursor.callproc(proc_name, tuple_list)
            row = cursor.fetchone()
            if row:
                cursor.close()
                self._db_conn.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            logging.error(traceback.format_exc())
            self.reconnect()
            self.call_proc_db(proc_name, tuple_list)
        except Exception, e:
            cursor.close()
            logging.error(traceback.format_exc())

