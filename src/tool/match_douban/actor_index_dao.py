# -*- coding:utf-8 -*-
import logging
from util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class ActorIndexDao(object):

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._tb_name = "douban_actor_index" 
    
    def check_actor(self, show_id, actor):
        try:
            sql = "SELECT id FROM %s WHERE show_id = %%s and actor = %%s" % (self._tb_name, )
            para =  (show_id, actor)
            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]

        except Exception, e:
            logging.error(traceback.format_exc())

    def store_actor(self, show_id, actor):
        try:
            sql = "INSERT INTO %s (show_id, actor) VALUES (%%s, %%s)" % (self._tb_name, )
            para = (show_id, actor)
            self._db_conn.execute_sql(sql, para)

        except Exception, e:
            logging.error(traceback.format_exc())
    
    def get_actor_by_did(self, did):
        try:
            sql = "SELECT actor FROM %s WHERE show_id = %%s" % (self._tb_name, )
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
            actor_index_dao =  ActorIndexDao(db_conn)
            '''
            d = u'中国'
            s = u'CCDD'
            if not actor_index_dao.check_actor(s, d):
                actor_index_dao.store_actor(s, d)
            '''
            actors = actor_index_dao.get_actor_by_did('1963104')
            logging.info(','.join(actors))

            db_conn.commit()
            db_conn.close()
    except Exception,e:
        logging.error(traceback.format_exc())
