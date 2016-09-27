#!/bin/env python
# -*- coding: utf-8    -*- 

import MySQLdb
import threading
import etc
import log

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DBConnect(object):
   
   def __init__(self):
       self.__conn = MySQLdb.connect(host=etc.host, user=etc.user, passwd=etc.passwd,db=etc.db, port=etc.port, charset = 'utf8')
       self.__cursor = self.__conn.cursor(cursorclass=MySQLdb.cursors.Cursor)

   def retry_connect(self):
       self.__conn = MySQLdb.connect(host=etc.host, user=etc.user, passwd=etc.passwd,db=etc.db, charset = 'utf8')
       self.__cursor = self.__conn.cursor()

   def  get_cursor(self):
       return self.__cursor

   def  get_dict_cursor(self):
       return self.__conn.cursor(MySQLdb.cursors.DictCursor)

   def close(self):
       try:
           if self.__cursor:
               self.__cursor.close()
           self.__conn.close()
       except Exception,e:
           print 'close error.',e
           #self.__dbconn_error.logerror("close error, has except: " % str(e))
           return False
       return True

   def db_fetchall(self, sql, param=None):
       try:
           result = []
           if param is None:
                count = self.__cursor.execute(sql)
           else:
                count = self.__cursor.execute(sql,param)
           if count>0:
                result = self.__cursor.fetchall()
           return result
       except (AttributeError, MySQLdb.OperationalError):
           print 'error with db_fethall.'
           #self.retry_connect()
           #print MySQLdb.OperationalError
           #return self.db_fetchall(sql, param)
       except Exception,e:
           print 'db_fetchall error.',e
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
               print key,", " , value_dict[key]
           insert_str = "INSERT INTO %s(%s) VALUES(%s)" % (table_name , ','.join(databasekeys), ','.join(['%s'] * len(databasekeys)))
           try:
               counter = self.__cursor.execute(insert_str, values)
               return counter
           except Exception,e:
               #print '_db_insert', e
               #self.__dbconn_error.logerror("_db_insert error." % (str(e)))
               return False
           return True
       except Exception,e:
           print '_db_insert', e
           #self.__dbconn_error.logerror("_db_insert error" % (str(e)))
           return False

   def __getInsertId(self):
        """
        获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self.__cursor.execute("SELECT @@IDENTITY AS id")
        result = self.__cursor.fetchall()
        return result[0]['id']

   def __query(self, sql, param=None):
        try:
            if param is None:
                count = self.__cursor.execute(sql)
            else:
                count = self.__cursor.execute(sql,param)
            #self.__conn.commit()
            return count
        except Exception,e:
           print 'query error.',e
           #self.__dbconn_error.logerror("get_db_records error, has except: " % str(e))
           return None

   def db_update(self, sql, param=None):
        return self.__query(sql,param)

   def query_info(self, sql):
       try:
           count = self.__query(sql, None)
           return count
       except Exception,e:
           print 'query_key error.',e
           #self.__dbconn_error.logerror("get_db_records error, has except: " % str(e))
           return None
   
   def call_proc_db(self, proc_name, tuple_list):
       try:
           self.__cursor.callproc(proc_name, tuple_list)
           ret = self.__cursor.fetchone()
           return  ret
       except Exception,e:
           print 'call_proc_db error.',e
           #self.__dbconn_error.logerror("call_proc_db error, has except: " % str(e))
           return None

if __name__ == "__main__":
   dbconn = DBConnect.instance()
   #dbconn.connect()
   table_name = "ugc_video"
   dict = {}
   dict['tid'] = "X1223439067"
   dict['site'] = "yk"
   dict['title'] = u"中国title"
   dict['tags'] = "sdfsf"
   dict['channel'] = "sdfsfs"
   dict['description'] = "sdfsfsfsd"
   dict['priority'] = 3
   dict['uid'] = 9
   dict['vid'] = "V121"
   dbconn.add(table_name, dict)
   dbconn.close()



