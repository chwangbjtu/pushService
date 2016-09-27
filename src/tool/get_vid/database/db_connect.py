# -*- coding:utf-8 -*-
import MySQLdb
import traceback
import logging

class MysqlConnect(object):
    DB_HOST = '111.161.35.219';
    DB_USER = 'root';
    DB_PWD = 'rz33dpsk';
    DB_NAME = 'ugc';
    DB_PORT = 13306;

    def __init__(self, host=None, user=None, pwd=None, name=None, port=None):
        self._db_conn = None;
        if host:
            self.DB_HOST = host;
        if user:
            self.DB_USER = user;
        if pwd:
            self.DB_PWD = pwd;
        if name:
            self.DB_NAME = name;
        if port:
            self.DB_PORT = port;

        self.reconnect();

    def __del__(self):
        self.close();

    def close(self):
        if self._db_conn:
            self._db_conn.close();
            self._db_conn = None;

    def reconnect(self):
        try:
            self.close();
            self._db_conn = MySQLdb.connect(host=self.DB_HOST, user=self.DB_USER, passwd=self.DB_PWD,db=self.DB_NAME, port=self.DB_PORT, charset = 'utf8');
            self._db_conn.autocommit(False);
        except Exception,e:
            logging.error(traceback.format_exc());

    def commit(self):
        if self._db_conn:
            try:
                self._db_conn.commit();
                return True
            except Exception,e:
                self._db_conn.rollback();
                logging.error(traceback.format_exc());
                return False;

    def rollback(self):
        if self._db_conn:
            try:
                self._db_conn.rollback();
                return True
            except Exception,e:
                logging.error(traceback.format_exc());
                return False;

    def execute_sql(self, sql, para=None, many=False):
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor();
                if para:
                    if many:
                        number = cursor.executemany(sql, para);
                    else:
                        number = cursor.execute(sql, para);
                else:
                    number = cursor.execute(sql);
                cursor.close();
                return number;
            except Exception, err:
                cursor.close();
                logging.error(traceback.format_exc());
                #logging.error('%s---%s' % (sql, para));

    def db_fetchall(self, sql, para=None, as_dic=False):
        if self._db_conn:
            try:
                if as_dic:
                    cursor = self._db_conn.cursor(MySQLdb.cursors.DictCursor);
                else:
                    cursor = self._db_conn.cursor();
                if para:
                    cursor.execute(sql, para);
                else:
                    cursor.execute(sql);
                result = cursor.fetchall();
                cursor.close();
                return result;
            except Exception, err:
                cursor.close();
                logging.error(traceback.format_exc());
                #logging.error('%s---%s' % (sql, para));

    def call_proc_db(self, proc_name, tuple_list):
        if self._db_conn:
            try:
                cursor = self._db_conn.cursor();
                cursor.callproc(proc_name, tuple_list);
                row = cursor.fetchone();
                if row:
                    cursor.close();
                    self._db_conn.commit();
            except Exception,e:
                cursor.close();
                logging.error(traceback.format_exc());

import os
import datetime

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect(name="ugc_test");
        if db_conn:
            dat_id = u"0000A7788C43791A787AB237C5E4AEAB79475D95";
            sql = "select * from ugc_dat where dat_id='%s'" % dat_id;
            results = db_conn.db_fetchall(sql);
            
            for row in results:
                dat_id          =   row[0];
                dat_size        =   row[1];
                mserver_ip      =   row[2];
                mserver_port    =   row[3];
                # print the result one by one 
                print "dat_id=%s, dat_size=%s, mserver_ip=%s, mserver_port=%s" % (dat_id, dat_size, mserver_ip, mserver_port);

            #raise MySQLdb.Error
            db_conn.commit();
            db_conn.close();
    except Exception,e:
        logging.error(traceback.format_exc());
