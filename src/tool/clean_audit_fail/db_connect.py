# -*- coding:utf-8 -*-
import MySQLdb
import traceback
import logging

class MysqlConnect(object):
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PWD = 'rz33dpsk'
    DB_NAME = 'ugc'
    DB_PORT = 13306

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
            self._db_conn = MySQLdb.connect(host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PWD,db=self.DB_NAME, port=self.DB_PORT, charset = 'utf8')
            self._db_conn.autocommit(False)
        except Exception,e:
            logging.info(traceback.format_exc())

    def commit(self):
        if self._db_conn:
            try:
                self._db_conn.commit()
                return True
            except Exception,e:
                self._db_conn.rollback()
                logging.info(traceback.format_exc())
                return False

    def rollback(self):
        if self._db_conn:
            try:
                self._db_conn.rollback()
                return True
            except Exception,e:
                logging.info(traceback.format_exc())
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
            except Exception, err:
                cursor.close()
                logging.info(traceback.format_exc())
                logging.info('%s: %s' % (sql, para))

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
            except Exception, err:
                cursor.close()
                logging.info(traceback.format_exc())
                logging.info('%s: %s' % (sql, para))

    def call_proc_db(self, proc_name, tuple_list):
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor()
                cursor.callproc(proc_name, tuple_list)
                row = cursor.fetchone()
                if row:
                    cursor.close()
                    self._db_conn.commit()
            except Exception,e:
                cursor.close()
                cursor.close()
