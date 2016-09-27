# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class TitleIndexDao(object):

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "douban_title_index" 
    
    def check_title(self, show_id, md5):
        try:
            sql = "SELECT title FROM %s WHERE show_id = %%s and md5 = %%s" % (self._tb_name, )
            para =  (show_id, md5)
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]

        except Exception, e:
            logging.error(traceback.format_exc())
    
    def get_did_by_title(self, md5):
        try:
            sql = "SELECT show_id FROM %s WHERE md5 = %%s" % (self._tb_name, )
            para =  (md5,)
            res = self._db_conn.db_fetchall(sql, para)
            ret = []
            if res:
                for r in res:
                    ret.append(r[0])
            return ret

        except Exception, e:
            logging.error(traceback.format_exc())

    def get_title_by_did(self, did):
        try:
            sql = "SELECT title FROM %s WHERE show_id = %%s" % (self._tb_name, )
            para =  (did,)
            res = self._db_conn.db_fetchall(sql, para)
            ret = []
            if res:
                for r in res:
                    ret.append(r[0])

            return ret

        except Exception, e:
            logging.error(traceback.format_exc())

    def store_title(self, title, show_id, md5):
        try:
            sql = "INSERT INTO %s (title, show_id, md5) VALUES (%%s, %%s, %%s)" % (self._tb_name, )
            para = (title, show_id, md5)
            self._db_conn.execute_sql(sql, para)

        except Exception, e:
            logging.error(traceback.format_exc())
    
if __name__ == "__main__":
    try:
        logger_init()
        db_conn = MysqlConnect(name="xv")
        if db_conn:
            title_index_dao =  TitleIndexDao(db_conn)

            #title_index_dao.store_title(u'中古', u'XVDDDD', u'111')

            titles = title_index_dao.get_title_by_did('5289175')
            logging.info(','.join(titles))

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
