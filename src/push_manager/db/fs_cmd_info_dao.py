# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')

class FsCmdInfoDao(object):

    def __init__(self, mysql_connect):
        self._table = 'fs_cmd_info'
        self._mysql_connect = mysql_connect

    def query_field(self, cmd_id, field):
        try:
            if cmd_id and field:
                sql = 'select %s from %s where cmd_id=%s' % (field, self._table, cmd_id)
                res = self._mysql_connect.db_fetchall(sql)
                if res:
                    return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc())
            return None
