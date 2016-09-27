import json
import traceback
from tornado import log
from db_connect import MysqlConnect

class BlacklistDao(object):
    
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._tb_name = "blacklist"

    def get_blacklist_words(self):
        try:
           sql = "select word from %s" % (self._tb_name,)
           para = None
           result = self._db_conn.db_fetchall(sql, para, as_dic=True)
           if result:
                return result
           else:
                return []
        except Exception, e:
            log.app_log.error("get blacklist exception: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s para:%s" % (sql, para))
    
    def insert(self, word, type=0):
        try:
            sql = "insert into %s (word, type) values(%%s, %%s)" % (self._tb_name,)
            para = (word, type)
            #print "insert (tb_name, word, type): (%s, %s, %s)" % (self._tb_name, word, _type)
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("insert new word(%s) into blacklist exception : %s" % (word,  e))
            log.app_log.debug("sql:%s para:%s" % (sql, para))
    
    def delete(self, word):
        try:
            sql = "delete from %s where word=%%s" % (self._tb_name,)
            para = (word,)
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("delete word(%s) from blacklist exception : %s" % (word,  e))
            log.app_log.debug("sql:%s para:%s" % (sql, para))

if __name__ == "__main__":
    try:
        db_conn = MysqlConnect()
        if db_conn:
            blacklist_dao = BlacklistDao(db_conn)

            blacklist_words = blacklist_dao.get_blacklist_words()

            for item in blacklist_words:
                log.app_log.info(item)

            db_conn.commit()
            db_conn.close()
    except Exception, e:
        log.app_log.error(traceback.format_exc())

