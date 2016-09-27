# -*- coding:utf-8 -*-
import traceback
from db_connect import MysqlConnect
import math
import json
import logging

class Dao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn

    def get_fail_task(self, since=None):
        try:
            sql = "select u.tid, u.task_id from ugc_video as u left join audit_fail as f on u.tid = f.tid where u.step = 'audit' and u.status = '2' and f.tid is null "
            if since:
                sql += "and u.mtime < '%s'" % since
            res = self._db_conn.db_fetchall(sql, as_dic=True)
            return res
        except Exception, e:
            logging.info(traceback.format_exc())
    
    def insert_fail(self, value_dict):
        try:
            keys = value_dict.keys()
            values = value_dict.values()
            sql = "INSERT INTO audit_fail (%s, ctime) VALUES (%s, now())" % (
                    ",".join(keys),
                    ",".join(['%s'] * len(keys)))
            para = values
            self._db_conn.execute_sql(sql, para)
        except Exception, e:
            logging.info(traceback.format_exc())

if __name__ == "__main__":
    try:
        from util import logger_init
        from util import get_date_since

        logger_init()

        db_conn = MysqlConnect()

        dao = Dao(db_conn)

        res = dao.get_fail_task(get_date_since(2))
        if res:
            logging.info('fail task: %s' % json.dumps(res))
        '''
        af = {'tid': '233', 'task_id': '233'}
        dao.insert_fail(af)
        db_conn.commit()
        '''

    except Exception,e:
        logging.info(traceback.format_exc())
