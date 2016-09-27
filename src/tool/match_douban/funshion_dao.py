# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class FunshionDao(object):

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "funshion" 

    def get_video(self):
        try:
            sql = "SELECT media_id, name, director, actor FROM %s" % (self._tb_name, )
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
            funshion_dao =  FunshionDao(db_conn)

            videos = funshion_dao.get_video()
            for v in videos:
                logging.info(json.dumps(v))

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
