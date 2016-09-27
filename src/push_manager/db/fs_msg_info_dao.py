# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')

class FsMsgInfoDao(object):

    def __init__(self, mysql_connect):
        self._table = 'fs_msg_info'
        self._mysql_connect = mysql_connect

    def update(self, msg_id, dict_data):
        try:
            keys = dict_data.keys()
            values = dict_data.values()
            sql = "update %s set %s where msg_id=%%s" % (self._table, ','.join(['%s=%%s' % k for k in keys]))
            para = list(values)
            para.append(msg_id)
            return self._mysql_connect.execute_sql(sql, para)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def insert(self, dict_data):
        try:
            keys = dict_data.keys()
            values = dict_data.values()
            sql = "insert into %s (%s) values (%s)" % (self._table, ",".join(keys), ",".join(['%s'] * len(keys)))
            para = values
            return self._mysql_connect.execute_sql(sql, para)
        except Exception, e:
            log.app_log.error(traceback.format_exc())
        

    def delete(self, msg_id=None):
        try:
            if msg_id:
                sql = 'delete from %s where msg_id=%s' % (self._table, msg_id)
                return self._mysql_connect.execute_sql(sql)
            else:
                pass
                #sql = 'delete from %s' % (self._table,)
                #return self._mysql_connect.execute_sql(sql)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def query(self, msg_id=None):
        try:
            if msg_id:
                sql = 'select * from %s where msg_id=%s' % (self._table, msg_id)
            else:
                sql = 'select * from %s' % (self._table,)
            res = self._mysql_connect.db_fetchall(sql, as_dic=True)
            if res:
                return res
            else:
                return []
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return []

    def query_field(self, msg_id, field):
        try:
            if msg_id and field:
                sql = 'select %s from %s where msg_id=%s' % (field, self._table, msg_id)
                res = self._mysql_connect.db_fetchall(sql)
                if res:
                    return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None
