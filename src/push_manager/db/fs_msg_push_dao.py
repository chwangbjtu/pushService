# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')

class FsMsgPushDao(object):

    def __init__(self, mysql_connect):
        self._table = 'fs_msg_push'
        self._mysql_connect = mysql_connect

    def update(self, push_id, dict_data):
        try:
            keys = dict_data.keys()
            values = dict_data.values()
            sql = "update %s set %s where push_id=%%s" % (self._table, ','.join(['%s=%%s' % k for k in keys]))
            para = list(values)
            para.append(push_id)
            return self._mysql_connect.execute_sql(sql, para)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def update_by_msgid_appid(self, msg_id, app_id, dict_data):
        try:
            keys = dict_data.keys()
            values = dict_data.values()
            sql = "update %s set %s where msg_id=%%s and app_id=%%s" % (self._table, ','.join(['%s=%%s' % k for k in keys]))
            para = list(values)
            para.append(msg_id)
            para.append(app_id)
            return self._mysql_connect.execute_sql(sql, para)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def update_by_msgid(self, msg_id, dict_data):
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
        

    def delete(self, push_id=None):
        try:
            if push_id:
                sql = 'delete from %s where push_id=%s' % (self._table, push_id)
                return self._mysql_connect.execute_sql(sql)
            else:
                pass
                #sql = 'delete from %s' % (self._table,)
                #return self._mysql_connect.execute_sql(sql)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def query(self, push_id=None):
        try:
            if push_id:
                sql = 'select * from %s where push_id=%s' % (self._table, push_id)
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

    def query_by_msgid_appid(self, msg_id, app_id):
        try:
            if msg_id and app_id:
                sql = 'select * from %s where msg_id=%s and app_id=%s' % (self._table, msg_id, app_id)
                res = self._mysql_connect.db_fetchall(sql, as_dic=True)
                if res:
                    return res
                else:
                    return []
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return []

    def query_field(self, push_id, field):
        try:
            if push_id and field:
                sql = 'select %s from %s where push_id=%s' % (field, self._table, push_id)
                res = self._mysql_connect.db_fetchall(sql)
                if res:
                    return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None

    def get_maxid(self):
        try:
            sql = 'select max(push_id) from %s' % (self._table)
            res = self._mysql_connect.db_fetchall(sql)
            if res:
                return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None
