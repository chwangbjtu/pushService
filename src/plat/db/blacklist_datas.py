# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from plat.settings import DATABASES
import traceback
import threading
import logging
logger = logging.getLogger('my')

class BLDatas(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect(host=DATABASES['default']['HOST'],
                                    user=DATABASES['default']['USER'],
                                    passwd=DATABASES['default']['PASSWORD'],
                                    db=DATABASES['default']['NAME'],
                                    port=int(DATABASES['default']['PORT']))
        self._db_conn = db_conn
        #self._video_tb_name = 'episode'

    @staticmethod
    def instance():
        if not hasattr(BLDatas, "_instance"):
            with BLDatas._instance_lock:
                if not hasattr(BLDatas, "_instance"):
                    BLDatas._instance = BLDatas()
        return BLDatas._instance
            
    def get_blcr_video(self, page, count):
        with BLDatas._instance_lock:
            try:
                sql = "SELECT * FROM blacklist"
                     
                sql += " where type='1'"
                sql += " order by id desc"
                ''' 
                if status and status != '5':
                    sql += " left join send_result on episode.show_id = send_result.show_id "
                 
                sql += " where true "
                
                if cond and content:
                    if cond == "title":
                        sql += " AND episode.title LIKE '%%%s%%'" % content
                    if cond == "user_name":
                        sql += " AND owner.user_name LIKE '%%%s%%'" % content
                    if cond == "owner":
                        sql += " AND owner.show_id = '%s'" % content
                    if cond == "keyword":
                        sql += " AND episode.show_id IN (SELECT show_id FROM keyword_episode WHERE kw_id = '%s')" % content
                    if cond == "page":
                        sql += " AND episode.show_id IN (SELECT show_id FROM page_episode WHERE pg_id = '%s')" % content
                    if cond == "cat":
                        sql += " AND episode.show_id IN (SELECT show_id FROM cat_list_episode WHERE cat_id = '%s')" % content
                    if cond == "subject":
                        sql += " AND episode.show_id IN (SELECT show_id FROM subject_episode WHERE subject_id = '%s')" % content
                        
                if origin:
                    sql += " AND episode.site_id = '%s'" %(origin)
                if classifi: 
                    sql += " AND episode.category = '%s'" %(classifi)
                if status == '5':
                    sql += " AND episode.show_id not in (select show_id from send_result) "
                elif status:
                    sql += " AND send_result.status_id = '%s'" %(status)
                    
                if order:
                    sql += " order by episode.%s desc " %(order)
                else:
                    sql += " order by episode.create_time desc"
                '''
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_blcr_video_count(self):
        with BLDatas._instance_lock:
            try:
                sql = "SELECT count(id) FROM blacklist "
                sql += " where type='1' "
                '''
                if cond:
                    sql += " left join owner on episode.owner_show_id=owner.show_id "
                
                sql += " WHERE true "
                if origin:
                    sql += " AND episode.site_id = '%s'" %(origin)
                if classifi: 
                    sql += " AND episode.category = '%s'" %(classifi)
                if status == '5':
                    sql += " AND episode.show_id not in (select show_id from send_result)"
                elif status:
                    sql += " AND episode.show_id in (select show_id from send_result where status_id = '%s')" % (status,)
                
                if cond and content:
                    if cond == "title":
                        sql += " AND episode.title LIKE '%%%s%%'" % content
                    if cond == "user_name":
                        sql += " AND owner.user_name LIKE '%%%s%%'" % content
                    if cond == "owner":
                        sql += " AND owner.show_id = '%s'" % content
                    if cond == "keyword":
                        sql += " AND episode.show_id IN (SELECT show_id FROM keyword_episode WHERE kw_id = '%s')" % content
                    if cond == "page":
                        sql += " AND episode.show_id IN (SELECT show_id FROM page_episode WHERE pg_id = '%s')" % content
                    if cond == "cat":
                        sql += " AND episode.show_id IN (SELECT show_id FROM cat_list_episode WHERE cat_id = '%s')" % content
                    if cond == "subject":
                        sql += " AND episode.show_id IN (SELECT show_id FROM subject_episode WHERE subject_id = '%s')" % content
                '''     
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
            
    def get_blpl_video(self, page, count):
        with BLDatas._instance_lock:
            try:
                sql = "SELECT * FROM blacklist"                     
                sql += " where type='0' "
                sql += " order by id desc"
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_blpl_video_count(self):
        with BLDatas._instance_lock:
            try:
                sql = "SELECT count(id) FROM blacklist "
                sql += " where type='0' "
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
            
    def add_blacklist(self, bl_word, bl_type):
        with BLDatas._instance_lock:
            try:
                sql = "insert into blacklist (word, type) values(%s, %s)"
                para = (bl_word, bl_type)
                
                #print sql
                res = self._db_conn.db_fetchall(sql, para)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def del_blacklist(self, bl_id):
        with BLDatas._instance_lock:
            try:
                sql = "delete from blacklist where id='%s'"%(bl_id)
                
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
   
