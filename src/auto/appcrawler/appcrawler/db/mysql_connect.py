# -*- coding:utf-8 -*-
import MySQLdb
import traceback
import logging
import time
import db_conf

class MysqlConnect(object):
    def __init__(self):
        self._db_conn = None
        self._db_host = db_conf.db_host
        self._db_user = db_conf.db_user
        self._db_pwd = db_conf.db_pwd
        self._db_name = db_conf.db_name
        self._db_port = db_conf.db_port
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
            self._db_conn = MySQLdb.connect(host=self._db_host, user=self._db_user, passwd=self._db_pwd, db=self._db_name, port=self._db_port, charset = 'utf8')
            self._db_conn.autocommit(False)
            return True
        except:
            return False

    def reconnect(self):
        try:
            while True:
                if not self.ping():
                    logging.log(logging.INFO, '++reconnected db')
                    self.connect()
                else:
                    break
                time.sleep(1)
                
        except Exception,e:
            logging.log(logging.ERROR, traceback.format_exc())

    def commit(self):
        try:
            self._db_conn.commit()
            return True
        except Exception, e:
            self.rollback()
            logging.log(logging.ERROR, traceback.format_exc())
            return False

    def rollback(self):
        try:
            self._db_conn.rollback()
            return True
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())
            return False

    def execute_sql(self, sql, para=None):
        try:
            self.reconnect()
            cursor = self._db_conn.cursor()
            if para:
                cursor.execute(sql, para)
            else:
                cursor.execute(sql)
            cursor.close()
        except (AttributeError, MySQLdb.OperationalError), e:
            cursor.close()
            logging.log(logging.INFO, "db exception: %s" % (str(e),))
            logging.log(logging.INFO, '%s: %s' % (sql, para))
        except Exception, e:
            cursor.close()
            logging.log(logging.ERROR, traceback.format_exc())
            logging.log(logging.INFO, '%s: %s' % (sql, para))

    def db_fetchall(self, sql, para=None, as_dic=False):
        try:
            self.reconnect()
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
            cursor.close()
            logging.log(logging.INFO, "db exception: %s" % (str(e),))
            logging.log(logging.INFO, '%s: %s' % (sql, para))
        except Exception, e:
            cursor.close()
            logging.log(logging.ERROR, traceback.format_exc())
            logging.log(logging.INFO, '%s: %s' % (sql, para))

    def call_proc_db(self, proc_name, tuple_list):
        try:
            self.reconnect()
            cursor = self._db_conn.cursor()
            cursor.callproc(proc_name, tuple_list)
            row = cursor.fetchone()
            if row:
                cursor.close()
                self._db_conn.commit()
        except (AttributeError, MySQLdb.OperationalError), e:
            cursor.close()
            logging.log(logging.INFO, "db exception: %s" % (str(e),))
        except Exception, e:
            cursor.close()
            logging.log(logging.ERROR, traceback.format_exc())


if __name__ == "__main__":
    pass

