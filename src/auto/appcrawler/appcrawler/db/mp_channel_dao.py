# -*- coding:utf-8 -*-
import traceback
import logging

class MpChannelDao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn

    def get_miaopai_task(self):
        try:
            sql = "select mpc_id, mpc_name from mp_channel where is_crawl = %s"
            para = (0,)
            res = self._db_conn.db_fetchall(sql, para, False)
            if res:
                return res
            else:
                return []
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())


if __name__ == "__main__":
    from mysql_connect import MysqlConnect
    try:
        dao = MpChannelDao(MysqlConnect())
        res = dao.get_miaopai_task()
        print res
    except Exception,e:
        logging.log(logging.ERROR, traceback.format_exc())
