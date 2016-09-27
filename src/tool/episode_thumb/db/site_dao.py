import json
import traceback
from tornado import log
from db_connect import MysqlConnect

class SiteDao(object):

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._tb_name = 'site'

    def get_sites(self):
       try:
            sql= "select site_id, site_code, site_name from %s" % self._tb_name
            para = (None)
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()
            return res
       except Exception, e:
            log.app_log.error("get sites excetpion: %s" % traceback.format_exc())
            log.app_log.debug("sql:%s  para:%s", (sql, para))

    def close(self):
        if self._db_conn:
            self._db_conn.close()
            
if __name__ == "__main__":
    try:
        db_conn = MysqlConnect()
        if db_conn:
            site_dao = SiteDao(db_conn)
            res = site_dao.get_sites()
            log.app_log.debug(res)
    except Exception, e:
        log.app_log.error("Exception: %s" % traceback.format_exc())
