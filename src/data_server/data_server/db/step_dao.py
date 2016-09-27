# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from tornado import log
import traceback

class StepDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._step_tb_name = 'step'

    def get_step_dic(self):
        try:
            sql = "SELECT step_id, step_name FROM %s" % (self._step_tb_name, )
            para = None
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)

            return {r['step_name']: r['step_id'] for r in res if 'step_name' in r and 'step_id' in r}

        except Exception, e:
            log.app_log.error("Get episode exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))
    
if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        step_dao = StepDao(db_conn)

        res = step_dao.get_step_dic()
        if res:
            log.app_log.debug(' '.join(['%s: %s' % (k, v ) for k, v in res.items()]))
        db_conn.commit()

    except Exception,e:
        log.app_log.error(traceback.format_exc())
