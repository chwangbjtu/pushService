# -*- coding:utf-8 -*-
import MySQLdb
import traceback
import logging

class MysqlConnect(object):
    DB_HOST = '127.0.0.1'
    DB_USER = 'spider'
    DB_PWD = 'fx.spider.242'
    DB_NAME = 'xv'
    DB_PORT = 13306

    def __init__(self, host=None, user=None, pwd=None, name=None, port=None):
        self._db_conn = None
        if host:
            self.DB_HOST = host
        if user:
            self.DB_USER = user
        if pwd:
            self.DB_PWD = pwd
        if name:
            self.DB_NAME = name
        if port:
            self.DB_PORT = port

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
            logging.error(traceback.format_exc())

    def commit(self):
        if self._db_conn:
            try:
                self._db_conn.commit()
                return True
            except Exception,e:
                self._db_conn.rollback()
                logging.error(traceback.format_exc())
                return False

    def rollback(self):
        if self._db_conn:
            try:
                self._db_conn.rollback()
                return True
            except Exception,e:
                logging.error(traceback.format_exc())
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
                logging.error(traceback.format_exc())
                logging.error('%s---%s' % (sql, para))

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
                logging.error(traceback.format_exc())
                logging.error('%s---%s' % (sql, para))

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
                logging.error(traceback.format_exc())

import os
import datetime

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            show_id = u'XNzEzODc3ODI0\\/\''
            title = u'评论比视频更精彩！'
            sql = "insert into douban_title_index (title, show_id) values (%s, %s)"
            para = (title, show_id)
            db_conn.execute_sql(sql, para, )

            #raise MySQLdb.Error
            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
