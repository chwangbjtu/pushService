#!/bin/env python
# -*- coding: utf-8    -*- 
import logging
import MySQLdb
import threading
import etc
import constant
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DBConnect(object):
    _mutex = threading.Lock()
   
    def __init__(self):
        self.__conn = MySQLdb.connect(host = etc.host, user = etc.user, passwd = etc.passwd, db = etc.db, port = etc.port, charset = 'utf8')
        self.__cursor = self.__conn.cursor(cursorclass = MySQLdb.cursors.Cursor)

    def retry_connect(self):
        self.__conn = MySQLdb.connect(host = etc.host, user = etc.user, passwd = etc.passwd, db = etc.db, charset = 'utf8')
        self.__cursor = self.__conn.cursor()

    def  get_cursor(self):
        return self.__cursor

    def close(self):
        try:
            logging.debug("close database connection ... ")
            self.__cursor.close()
            self.__conn.close()
        except Exception, err:
            logging.warning("exception when closing database %s", str(err))
            return False
        return True

    def db_fetchall(self, sql, param=None):
        logging.debug("run sql %s with param %s", sql, str(param))
        try:
            result = []
            if param is None:
                count = self.__cursor.execute(sql)
            else:
                count = self.__cursor.execute(sql, param)
            if count > 0:
                result = self.__cursor.fetchall()
            return result
        except (AttributeError, MySQLdb.OperationalError):
            logging.warning("exception when fetching record with sql %s, %s", sql, str(MySQLdb.OperationalError))
            #self.retry_connect()
            #self.db_fetchall(sql, param)
            return None
        except Exception, err:
            logging.warning("exception when fetching record with sql %s, %s", sql, str(err))
            return None

    '''
    @param table_name: 数据库表名称
    @param value_dict:要插入的记录数据tuple/list
    '''
    def db_insert(self, table_name, value_dict):
        try:
            values = []                                                                                  
            databasekeys = []
            for key in value_dict:
                databasekeys.append(key)
                values.append(value_dict[key])
            insert_str = "INSERT INTO %s(%s) VALUES(%s)" % (table_name, ','.join(databasekeys), ','.join(['%s'] * len(databasekeys)))
            try:
                logging.debug("run sql %s with values %s", insert_str, str(values))
                counter = self.__cursor.execute(insert_str, values)
                return (constant.SUCCESS, counter)
            except Exception, err:
                logging.warning("exception when running sql %s, %s", insert_str, str(err))
                return (constant.FAIL, str(err))
        except Exception, err:
            logging.warning("exception when inserting table %s, %s", table_name, str(err))
            return (constant.FAIL, str(err))

    def __getInsertId(self):
        '''
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        '''
        logging.debug("run sql SELECT @@IDENTITY AS id")
        self.__cursor.execute("SELECT @@IDENTITY AS id")
        result = self.__cursor.fetchall()
        return result[0]['id']

    def __query(self, sql, param=None):
        try:
            logging.debug("run sql %s with param %s", sql, str(param))
            if param is None:
                count = self.__cursor.execute(sql)
            else:
                count = self.__cursor.execute(sql, param)
            return count
        except Exception, err:
            logging.warning("exception when running sql %s and param %s, %s", sql, str(param), str(err))
            return None

    def db_update(self, sql, param=None):
        return self.__query(sql, param)

    def query_info(self, sql):
        try:
            count = self.__query(sql, None)
            return count
        except Exception, err:
            logging.warning("exception when running sql %s, %s", sql, str(err))
            return None
   
    def call_proc_db(self, proc_name, tuple_list):
        try:
            logging.debug("call stored procedure %s", proc_name)
            self.__cursor.callproc(proc_name, tuple_list)
            self.__cursor.fetchone()
            return (constant.SUCCESS, True)
        except Exception, err:
            logging.warning("exception when calling stored procedure %s", proc_name)
            call_proc_err = "call_proc_db error proc_name:%s, error:%s" % (proc_name, str(err))
            return (constant.FAIL, call_proc_err)

if __name__ == "__main__":
    pass
    # dbconn = DBConnect()
    # connstr = "select * from ugc_video limit 1"
    # record = dbconn.db_fetchall(connstr)
    # print record
    # dbconn.close()

    # dbconn = DBConnect()
    # dict = {}
    # dict['dat_id'] = '123456'
    # dict['dat_size'] = '123'
    # dict['mserver_ip'] = '129.232.5.6'
    # dict['mserver_port'] = '1234'
    # dict['flag'] = '1'
    # key = []
    # key.append(dict['dat_id'])
    # sql = "select * from ugc_dat"
    # ret = dbconn.db_fetchall(sql)
    # print ret
    # dbconn.close()

    # dbconn = DBConnect()
    # proc_name = "proc_verify_ms_dat"
    # tid = 'X121121'
    # size = 346
    # ip = '100.23.90.44'
    # port = '99'
    # tuple_list = "('%s', %d, '%s', '%s')" % ('X121121',456, '100.23.90.44','9090')
    # print tuple_list
    # ret = dbconn.call_proc_db(proc_name, (tid, size, ip, port))
    # print ret
    # dbconn.close()

    # list = []
    # if len(list) == 0:
        # print 'list is null'
    # else:
        # print 'not null.'

    # dbconn = DBConnect()
    # dbconn = DBConnect()
    # connstr = "update ugc_dat set mserver_port=80 where dat_id = 'X121121'"
    # ret = dbconn.db_update(connstr)
    # print ret
    # dbconn.close()
    