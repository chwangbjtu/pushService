# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class FDRDao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "fdr" 

    def check_rel(self, fun_id, dou_id):
        try:
            sql = "SELECT id FROM %s WHERE fun_id = %%s and dou_id = %%s" % (self._tb_name, )
            para =  (fun_id, dou_id)
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]

        except Exception, e:
            logging.error(traceback.format_exc())

    def update_rel(self, fun_id, dou_id, fit):
        try:
            sql = "UPDATE %s SET fit = %%s WHERE fun_id = %%s and dou_id = %%s" % (self._tb_name, )
            para = (fit, fun_id, dou_id)
            self._db_conn.execute_sql(sql, para)

        except Exception, e:
            logging.error(traceback.format_exc())

    def store_rel(self, fun_id, dou_id, fit):
        try:
            sql = "INSERT INTO %s (fun_id, dou_id, fit) VALUES (%%s, %%s, %%s)" % (self._tb_name, )
            para = (fun_id, dou_id, fit)
            self._db_conn.execute_sql(sql, para)

        except Exception, e:
            logging.error(traceback.format_exc())
    
if __name__ == "__main__":
    try:
        logger_init()
        db_conn = MysqlConnect(name="xv")
        if db_conn:

            fdr_dao =  FDRDao(db_conn)
            (fd, dd, m) = (100, '200', 80)
            if not fdr_dao.check_rel(fd, dd):
                fdr_dao.store_rel(fd, dd, m)
            else:
                m = 50
                fdr_dao.update_rel(fd, dd, m)

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
