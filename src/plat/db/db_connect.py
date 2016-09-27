# -*- coding:utf-8 -*-
import MySQLdb
import traceback

import sys
import time
sys.path.append('.')

class MysqlConnect(object):

    def __init__(self,host,user,passwd,db,port):
        self._db_conn = None
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db
        self._port = port
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
            self._db_conn = MySQLdb.connect(host=self._host,
                                            user=self._user,
                                            passwd=self._passwd,
                                            db=self._db,
                                            port=int(self._port),
                                            charset='utf8')
            self._db_conn.autocommit(False)
            return True
        except:
            return False

    def reconnect(self):
        try:
            print '++reconnect db'
            while True:
                if not self.ping():
                    self.connect()
                else:
                    break
                time.sleep(1)
            print '++reconnected db'
                
        except Exception, e:
            print "Connect exception: %s" % traceback.format_exc()

    def commit(self):
        try:
            self._db_conn.commit()
            return True
        except Exception, e:
            self.rollback()
            print "Commit exception: %s" % traceback.format_exc()
            return False

    def rollback(self):
        try:
            self._db_conn.rollback()
            return True
        except Exception, e:
            print "Rollback exception: %s" % traceback.format_exc()
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
            print "db exception: %s" % (str(e),)
            self.reconnect()
            self.execute_sql(sql, para)
        except Exception, e:
            cursor.close()
            print "Execute sql : %s, exception: %s" % (sql, traceback.format_exc())

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
            print "db exception: %s" % (str(e),)
            self.reconnect()
            return self.db_fetchall(sql, para, as_dic)
        except Exception, e:
            cursor.close()
            print "Fetchall sql : %s, exception: %s" % (sql, traceback.format_exc())

    def call_proc_db(self, proc_name, tuple_list):
        try:
            cursor = self._db_conn.cursor()
            cursor.callproc(proc_name, tuple_list)
            row = cursor.fetchone()
            if row:
                cursor.close()
                self._db_conn.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            print "db exception: %s" % (str(e),)
            self.reconnect()
            self.call_proc_db(proc_name, tuple_list)
        except Exception, e:
            cursor.close()
            print "Call proc: %s, exception: %s" % (proc_name, traceback.format_exc())

