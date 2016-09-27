# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class DoubanDao(object):

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "douban" 

    def get_video(self):
        try:
            sql = "SELECT title, aka, director, actor, show_id FROM %s" % (self._tb_name, )
            para = None
            res = self._db_conn.db_fetchall(sql, as_dic=True)
            if res:
                return res
            return []

        except Exception, e:
            logging.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        logger_init()
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            douban_dao = DoubanDao(db_conn)

            videos = douban_dao.get_video()
            for v in videos:
                logging.info(json.dumps(v))

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
