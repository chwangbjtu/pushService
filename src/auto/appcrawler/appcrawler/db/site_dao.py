# -*- coding:utf-8 -*-
import traceback
import logging

class SiteDao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn

    def get_site_by_code(self, code):
        try:
            sql = "SELECT * from site WHERE site_code = %s"
            para = (code,)
            res = self._db_conn.db_fetchall(sql, para, True)
            if res:
                return res[0]
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())
            
    def insert_site(self, value_dict):
        try:
            keys = value_dict.keys()
            values = value_dict.values()
            sql = "INSERT INTO site (%s) VALUES (%s)" % (
                    ",".join(keys),
                    ",".join(['%s'] * len(keys)))
            para = values
            self._db_conn.execute_sql(sql, para)
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def get_site_id_by_code(self, code):
        try:
            sql = "SELECT site_id from site WHERE site_code = %s"
            para = (code, )
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())


if __name__ == "__main__":
    from mysql_connect import MysqlConnect
    try:
        db_conn = MysqlConnect()
        if db_conn:
            dao = SiteDao(db_conn)
            print dao.get_site_id_by_code('miaopai')
    except Exception,e:
        print e
