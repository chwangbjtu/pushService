# -*- coding:utf-8 -*-
import logging
import sys
sys.path.append("..")
from util.util import logger_init
import traceback
from db_connect import MysqlConnect
import json

class UgcdatDao(object):
    def __init__(self, db_conn):
        self._db_conn = db_conn;
        self._tb_name = "ugc_dat";

    def get_dat_ids(self):
        try:
            sql = "select dat_id from %s " % (self._tb_name,);
            results = self._db_conn.db_fetchall(sql, as_dic=True);
            if results:
                return results;
            return [];
        except Exception, e:
            logging.error(traceback.format_exc());

    def get_dat_ids_inc(self):
        try:
            sql = "select distinct(d.dat_id) as dat_id from ugc_video as u join ugc_fid_map as d on u.tid = d.tid where u.step = 'distribute' and u.status = '1' and u.video_id is null"
            results = self._db_conn.db_fetchall(sql, as_dic=True);
            if results:
                return results;
            return [];
        except Exception, e:
            logging.error(traceback.format_exc());
        
if __name__ == "__main__":
    try:
        logger_init();
        db_conn = MysqlConnect(name="ugc_test");
        if db_conn:
            ugc_dat_dao = UgcdatDao(db_conn);

            dat_ids = ugc_dat_dao.get_dat_ids();

            for dat_id in dat_ids:
                logging.info(json.dumps(dat_id));

            db_conn.commit();
            db_conn.close();
    except Exception, e:
        logging.error(traceback.format_exc());
