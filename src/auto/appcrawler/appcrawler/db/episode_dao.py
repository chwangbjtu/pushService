# -*- coding:utf-8 -*-
import traceback
import logging
import math

class EpisodeDao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = 'episode'

    def get_episode(self, cont_id, site_id):
        try:
            sql = "SELECT id from %s WHERE cont_id = %%s and site_id = %%s" % (
                    self._tb_name, )
            para = (cont_id, site_id)
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def insert_episode(self, value_dict):
        try:
            keys = value_dict.keys()
            values = value_dict.values()
            sql = "INSERT INTO %s (%s, ctime, mtime) VALUES (%s, now(), now())" % (
                    self._tb_name, 
                    ",".join(keys),
                    ",".join(['%s'] * len(keys)))
            para = values
            self._db_conn.execute_sql(sql, para)
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

    def update_episode(self, cont_id, site_id, value_dict):
        try:
            keys = value_dict.keys()
            values = value_dict.values()
            sql = "UPDATE %s SET %s, mtime=now() WHERE cont_id = %%s and site_id = %%s " % (
                    self._tb_name,
                    (",").join(['%s=%%s' % k for k in keys]))
            para = list(values)
            para.extend([cont_id, site_id])
            self._db_conn.execute_sql(sql, para)
        except Exception, e:
            logging.log(logging.ERROR, traceback.format_exc())

if __name__ == "__main__":
    from mysql_connect import MysqlConnect
    pass

