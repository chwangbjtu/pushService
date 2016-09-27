# -*- coding:utf-8 -*-
import time
import MySQLdb
import traceback
from tornado import log

import sys
sys.path.append('.')

class MysqlConnect(object):

    def __init__(self, host='', port='', user='', passwd='', db=''):
        self._host = host
        self._port = port
        self._user = user
        self._passwd = passwd
        self._db = db
        self._retry_times = 3

        self._mysql = None
        self.connect()

    def __del__(self):
        self.close()

    def connect(self):
        try:
            if self._mysql:
                pass
            elif self._host and self._port and self._user and self._passwd and self._db:
                self._mysql = MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd, db=self._db, charset = 'utf8')
            self._mysql.autocommit(False)
        except Exception, err:
            log.app_log.error(traceback.format_exc())

    def close(self):
        try:
            if self._mysql:
                self._mysql.close()
                self._mysql = None
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def ping(self):
        try:
            if self._mysql:
                self._mysql.ping()
                return True
            else:
                return False
        except Exception, e:
            return False

    def is_connected(self):
        return self.ping()

    def check_connected(self):
        res = False
        cnt = 0
        while cnt < self._retry_times:
            try:
                if self.ping():
                    res = True
                    break
                else:
                    log.app_log.info('++reconnected db')
                    self._mysql = None
                    self.connect()
                    pass
            except Exception,e:
                log.app_log.error(traceback.format_exc())
                time.sleep(0.5)
            finally:
                cnt = cnt + 1
        return res

    def commit(self):
        try:
            if not self.check_connected():
                return False
            self._mysql.commit()
            return True
        except Exception, e:
            self.rollback()
            log.app_log.error(traceback.format_exc())
            return False

    def rollback(self):
        try:
            if not self.check_connected():
                return False
            self._mysql.rollback()
            return True
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return False

    def insert_id(self):
        try:
            if not self.check_connected():
                return None
            id = self._mysql.insert_id()
            return id
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None

    def execute_sql(self, sql, para=None):
        try:
            if not self.check_connected():
                return None
            cursor = self._mysql.cursor()
            if para:
                res = cursor.execute(sql, para)
            else:
                res = cursor.execute(sql)
            cursor.close()
            return res
        except (AttributeError, MySQLdb.OperationalError), e:
            cursor.close()
            self.rollback()
            log.app_log.info("db exception: %s" % (str(e),))
            log.app_log.info('%s: %s' % (sql, para))
        except Exception, e:
            cursor.close()
            self.rollback()
            log.app_log.error(traceback.format_exc())
            log.app_log.info('%s: %s' % (sql, para))

    def db_fetchall(self, sql, para=None, as_dic=False):
        try:
            if not self.check_connected():
                return False
            if as_dic:
                cursor = self._mysql.cursor(MySQLdb.cursors.DictCursor)
            else:
                cursor = self._mysql.cursor()
            if para:
                cursor.execute(sql, para)
            else:
                cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except (AttributeError, MySQLdb.OperationalError), e:
            cursor.close()
            self.rollback()
            log.app_log.info("db exception: %s" % (str(e),))
            log.app_log.info('%s: %s' % (sql, para))
        except Exception, e:
            cursor.close()
            self.rollback()
            log.app_log.error(traceback.format_exc())
            log.app_log.info('%s: %s' % (sql, para))

    def call_proc_db(self, proc_name, tuple_list):
        try:
            if not self.check_connected():
                return False
            cursor = self._mysql.cursor()
            cursor.callproc(proc_name, tuple_list)
            row = cursor.fetchone()
            if row:
                cursor.close()
                self.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            cursor.close()
            self.rollback()
            log.app_log.info("db exception: %s" % (str(e),))
        except Exception, e:
            cursor.close()
            self.rollback()
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    test = MysqlConnect(host='192.168.177.3', port=3306, user='root', passwd='funshion', db='xv')
    res = test.execute_sql(sql='insert into category (cat_id, cat_name) values ("5", "测试")', para=None)
    test.commit()
    #test.rollback()
    print res
