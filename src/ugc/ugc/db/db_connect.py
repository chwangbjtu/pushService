# -*- coding:utf-8 -*-
import MySQLdb
import traceback

import sys
sys.path.append('.')
from ugc.settings import DATABASES

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
            self._db_conn = MySQLdb.connect(host=DATABASES['default']['HOST'],
                                            user=DATABASES['default']['USER'],
                                            passwd=DATABASES['default']['PASSWORD'],
                                            db=DATABASES['default']['NAME'],
                                            port=int(DATABASES['default']['PORT']),
                                            charset='utf8')
            self._db_conn.autocommit(False)
        except Exception, e:
            print "Connect exception: %s" % traceback.format_exc()

    def commit(self):
        if self._db_conn:
            try:
                self._db_conn.commit()
                return True
            except Exception, e:
                self._db_conn.rollback()
                print "Commit exception: %s" % traceback.format_exc()
                return False

    def rollback(self):
        if self._db_conn:
            try:
                self._db_conn.rollback()
                return True
            except Exception, e:
                print "Rollback exception: %s" % traceback.format_exc()
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
                #cursor.close()
                print "Execute sql : %s, exception: %s" % (sql, traceback.format_exc())

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
                #cursor.close()
                print "Fetchall sql : %s, exception: %s" % (sql, traceback.format_exc())
                #self.reconnect()
                #self.db_fetchall(sql, para, as_dic)

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
                self.call_proc_db(proc_name, tuple_list)
            except Exception, e:
                #cursor.close()
                print "Call proc: %s, exception: %s" % (proc_name, traceback.format_exc())
                #self.reconnect()
                #self.call_proc_db(proc_name, tuple_list)

import os
import datetime

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        if db_conn:
            sql = "select * from ugc_video order by ctime desc limit 1"
            res = db_conn.db_fetchall(sql, as_dic=True)
            if res:
                for r in res:
                    print ' '.join(['%s: %s' % (k, v ) for k, v in r.items()])

            db_conn.commit()
            db_conn.close()
    except Exception as e:
        print "Exception: %s" % traceback.format_exc()
