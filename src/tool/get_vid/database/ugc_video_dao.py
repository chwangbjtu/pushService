# -*- coding:utf-8 -*-

from db_connect import MysqlConnect
import json
import logging
import sys
sys.path.append(".")
from util.util import logger_init
import traceback

class UgcvideoDao(object):
    
    def __init__(self, db_conn):
        self._db_conn = db_conn;
        self._db_name = "ugc_video";

    def update_video_id(self, video_id, task_id):
        try:
            sql = "update %s set video_id = %%s where task_id = %%s" % (self._db_name,);
            # print sql;
            # print (video_id, task_id);
            para = (video_id, task_id);
            number = self._db_conn.execute_sql(sql, para);
            if number == None:
                logging.info("task_id: %s cannot be found in database" % task_id);
        except Exception, e:
            logging.error(traceback.format_exc());

    def export_video_id(self):
        try:
            sql = "select video_id from ugc_video where video_id is not null into outfile '/tmp/vid'"
            self._db_conn.execute_sql(sql);
        except Exception, e:
            logging.error(traceback.format_exc());

    def get_video_id(self):
        try:
            sql = "select dat_id from %s " % (self._tb_name,);
            results = self._db_conn.db_fetchall(sql, as_dic=True);
            if results:
                return results;
            return [];
        except Exception, e:
            logging.error(traceback.format_exc());

    def get_unsend_vid(self, count=1000):
        try:
            sql = "select u.video_id as vid, u.origin as origin, u.uid as uid from ugc_video as u left join video_id as v on u.video_id = v.vid where u.video_id is not null and v.vid is null limit %s" % count
            return self._db_conn.db_fetchall(sql, as_dic=True);
        except Exception, e:
            logging.error(traceback.format_exc());

    def set_send(self, vids):
        try:
            sql = "insert into video_id (vid) values (%s)"
            para = vids
            self._db_conn.execute_sql(sql, para, many=True);
        except Exception, e:
            logging.error(traceback.format_exc());


if __name__ == "__main__":
    try:
        logger_init();
        db_conn = MysqlConnect(name="ugc");
        if db_conn:
            ugc_video_dao = UgcvideoDao(db_conn);
            '''
            (video_id, task_id) = (None, "1");
            number = ugc_video_dao.update_video_id(video_id, task_id);
            '''
            '''
            ugc_video_dao.set_send(['1', '3', 5, 6])
            db_conn.commit();
            '''
            res = ugc_video_dao.get_unsend_vid(10000)

            cats = {"8800": [], "8801": [], "8802": [], "8803": []}
            for r in res:
                if str(r['uid']) == '9':
                    cats['8800'].append(r['vid'])
                elif r['origin'] == 'forwards':
                    cats['8801'].append(r['vid'])
                elif r['origin'] == 'upload' and str(r['uid']) != '9':
                    cats['8802'].append(r['vid'])
                elif r['origin'] == 'push':
                    cats['8803'].append(r['vid'])
            for k, v in cats.items():
                print '%s - %s' % (k, len(v))
            print 'total - %s' % sum([len(v) for v in cats.values()])

            db_conn.close();
    except Exception, e:
        logging.error(traceback.format_exc());
        
