#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from plat.settings import DATABASES
import traceback
import threading
import logging
logger = logging.getLogger('my')

class RepDatas(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect(host=DATABASES['default']['HOST'],
                                    user=DATABASES['default']['USER'],
                                    passwd=DATABASES['default']['PASSWORD'],
                                    db=DATABASES['default']['NAME'],
                                    port=int(DATABASES['default']['PORT']))
        self._db_conn = db_conn

    @staticmethod
    def instance():
        if not hasattr(RepDatas, "_instance"):
            with RepDatas._instance_lock:
                if not hasattr(RepDatas, "_instance"):
                    RepDatas._instance = RepDatas()
        return RepDatas._instance

    def get_site_list(self):
       with RepDatas._instance_lock:
            try:
                sql = "select site_name, site_id from site"
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def add_repost(self, uid, show_id, url, title, tags, desc, priority, channel, site_id):
       with RepDatas._instance_lock:
            try:
                sql = "insert into customer_episode (uid, show_id, site_id, title, category, tag,url, description, priority, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
                para = (uid, show_id, site_id, title, channel, tags, url, desc, priority)
                #其中type字段，默认值是1，所以转帖就不用写这个字段的值了
                
                self._db_conn.execute_sql(sql, para)
                self._db_conn.commit()
                return True
            except Exception, e:
                logger.error(traceback.format_exc())
                return False
                
    def get_repost_video(self, username, page, count):
        with RepDatas._instance_lock:
            try:
                sql = "select c_e.type, c_e.priority, c_e.title, c_e.category, c_e.tag, c_e.create_time, c_e.description, e_s.step_id, e_s.status from customer_episode as c_e"
                sql += " left join auth_user as a_u on c_e.uid = a_u.id "
                sql += " left join episode_status as e_s on (e_s.eid = c_e.id and e_s.origin = '1')"
                sql += " where true"
                
                sql += " and a_u.username = '%s'" % username
                
                sql += " order by c_e.create_time desc"
                sql += ' limit %s offset %s' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_repost_video_count(self, username):
        with RepDatas._instance_lock:
            try:
                sql = "select count(*) from customer_episode as c_e"
                sql += " left join auth_user as a_u on c_e.uid = a_u.id where a_u.username = '%s'"%username
                
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def add_upload_content(self, uid, show_id, title, tags, desc, priority, channel, audit, url):
       with RepDatas._instance_lock:
            try:
                sql = "insert into customer_episode (uid, type, show_id, site_id, title, category, tag, description, priority, audit, url, create_time) values (%s, '2', %s, '100', %s, %s, %s, %s, %s, %s, %s, now())"
                para = (uid, show_id, title, channel, tags, desc, priority, audit, url)
                #其中type字段，默认值是1，所以转帖就不用写这个字段的值了
                #print sql,para
                self._db_conn.execute_sql(sql, para)
                self._db_conn.commit()
                return True
            except Exception, e:
                logger.error(traceback.format_exc())
                return False

if __name__ == "__main__":

    ins = RepDatas.instance()
    print ins.get_site_list()
