# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
import logging
import traceback
import json

class EpisodeDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn

    def get_low_episode_since(self, since_time):
        try:
            sql = "SELECT id, url FROM episode WHERE create_time > %s and format_id < 2"
            para = [since_time,]
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()
            return res

        except Exception, e:
            logging.error("exception: %s " % traceback.format_exc())
    
    def update_format(self, eid, format_code):
        try:
            sql = "update episode set format_id = (select format_id from format where format_code = %s) where id = %s"
            para = (format_code, eid)
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()

        except Exception, e:
            logging.error("exception: %s " % traceback.format_exc())

if __name__ == "__main__":
    
    from util import Util

    try:
        Util.init_logger()
        db_conn = MysqlConnect()
        episode_dao = EpisodeDao(db_conn)

        '''
        res = episode_dao.get_low_episode_since('2015-1-27')
        if res:
            logging.info(json.dumps(res))
        '''

        episode_dao.update_format('1635449', 'super')
        db_conn.commit()

    except Exception,e:
        logging.error(traceback.format_exc())
