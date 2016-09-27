# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')

class FsAppInfoDao(object):

    def __init__(self, mysql_connect):
        self._table = 'fs_app_info'
        self._mysql_connect = mysql_connect

    def query(self, app_id=None):
        try:
            if app_id:
                sql = 'select * from %s where app_id=%s' % (self._table, app_id)
            else:
                sql = 'select * from %s' % (self._table,)
            res = self._mysql_connect.db_fetchall(sql, as_dic=True)
            if res:
                return res
            else:
                return []
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None

    def query_field(self, app_id, field):
        try:
            if app_id and field:
                sql = 'select %s from %s where app_id=%s' % (field, self._table, app_id)
                res = self._mysql_connect.db_fetchall(sql)
                if res:
                    return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None

    def query_field_by_app_name(self, app_name, field):
        try:
            if app_name and field:
                sql = 'select %s from %s where app_name="%s"' % (field, self._table, app_name)
                res = self._mysql_connect.db_fetchall(sql)
                if res:
                    return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None

    def query_by_app_name(self, app_name):
        try:
            if app_name:
                sql = 'select * from %s where app_name="%s"' % (self._table, app_name)
                res = self._mysql_connect.db_fetchall(sql, as_dic=True)
                if res:
                    return res[0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None
