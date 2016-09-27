# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class DirectorIndexDao(object):

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "douban_director_index" 
    
    def check_director(self, show_id, director):
        try:
            sql = "SELECT id FROM %s WHERE show_id = %%s and director = %%s" % (self._tb_name, )
            para =  (show_id, director)
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]

        except Exception, e:
            logging.error(traceback.format_exc())

    def store_director(self, show_id, director):
        try:
            sql = "INSERT INTO %s (show_id, director) VALUES (%%s, %%s)" % (self._tb_name, )
            para = (show_id, director)
            self._db_conn.execute_sql(sql, para)

        except Exception, e:
            logging.error(traceback.format_exc())

    def get_director_by_did(self, did):
        try:
            sql = "SELECT director FROM %s WHERE show_id = %%s" % (self._tb_name, )
            para =  (did,)
            res = self._db_conn.db_fetchall(sql, para)
            ret = []
            if res:
                for r in res:
                    ret.append(r[0])

            return ret

        except Exception, e:
            logging.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        logger_init()
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            director_index_dao =  DirectorIndexDao(db_conn)
            '''
            d = u'中国'
            s = u'CCDD'
            if not director_index_dao.check_director(s, d):
                director_index_dao.store_director(s, d)
            '''
            directors = director_index_dao.get_director_by_did('1785006')
            logging.info(','.join(directors))

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
