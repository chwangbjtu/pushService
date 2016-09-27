# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from plat.settings import DATABASES
import traceback
import threading
import logging
logger = logging.getLogger('my')

class UgcVideoDao(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect(host=DATABASES['default']['HOST'],
                                    user=DATABASES['default']['USER'],
                                    passwd=DATABASES['default']['PASSWORD'],
                                    db=DATABASES['default']['NAME'],
                                    port=int(DATABASES['default']['PORT']))
        self._db_conn = db_conn
        self._video_tb_name = 'episode'

    @staticmethod
    def instance():
        if not hasattr(UgcVideoDao, "_instance"):
            with UgcVideoDao._instance_lock:
                if not hasattr(UgcVideoDao, "_instance"):
                    UgcVideoDao._instance = UgcVideoDao()
        return UgcVideoDao._instance
            
    def get_episode_video(self, page, count, origin, classifi, status, order, cond, content):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT ep.id, ep.show_id,ep.owner_show_id,ep.title,ep.category,ep.site_id,ep.upload_time,ep.create_time,ep.url,owner.user_name,ep.played,eps.step_id,eps.status,fm.format_name "
                sql += " FROM episode as ep"
                     
                sql += " left join owner on ep.owner_show_id=owner.show_id "
                 
                sql += " left join episode_status as eps on (ep.id = eps.eid and eps.origin='0')"
                
                sql += " left join format as fm on ep.format_id = fm.format_id"
                 
                sql += " where true "
                
                if cond and content:
                    if cond == "title":
                        sql += " AND ep.title LIKE '%%%s%%'" % content
                    if cond == "user_name":
                        sql += " AND owner.user_name LIKE '%%%s%%'" % content
                    if cond == "owner":
                        sql += " AND owner.show_id = '%s'" % content
                    if cond == "keyword":
                        sql += " AND ep.show_id IN (SELECT show_id FROM keyword_episode WHERE kw_id = '%s')" % content
                    if cond == "page":
                        sql += " AND ep.show_id IN (SELECT show_id FROM page_episode WHERE pg_id = '%s')" % content
                    if cond == "cat":
                        sql += " AND ep.show_id IN (SELECT show_id FROM cat_list_episode WHERE cat_id = '%s')" % content
                    if cond == "subject":
                        sql += " AND ep.show_id IN (SELECT show_id FROM subject_episode WHERE subject_id = '%s')" % content
                        
                if origin:
                    sql += " AND ep.site_id = '%s'" %(origin)
                if classifi: 
                    sql += " AND ep.category = '%s'" %(classifi)
                if status == '8':
                    sql += " AND ep.show_id not in (select show_id from episode_status) "
                elif status:
                    sql += " AND eps.status = '%s'" %(status)
                    
                if order:
                    sql += " order by ep.%s desc " %(order)
                else:
                    sql += " order by ep.create_time desc"
     
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_episode_video_count(self, origin, classifi, status, cond, content):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT count(episode.show_id) FROM episode "

                if cond:
                    sql += " left join owner on episode.owner_show_id=owner.show_id "
                
                sql += " WHERE true "
                if origin:
                    sql += " AND episode.site_id = '%s'" %(origin)
                if classifi: 
                    sql += " AND episode.category = '%s'" %(classifi)
                if status == '8':
                    sql += " AND episode.show_id not in (select show_id from episode_status)"
                elif status:
                    sql += " AND episode.show_id in (select show_id from episode_status where status = '%s')" % (status,)
                
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
                     
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
                
    def get_youtube(self, page, count, order, status, cond, content, classifi):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT owner.id, owner.show_id, owner.user_name, owner.intro, owner.played, owner.fans, owner.url FROM owner " 
                if status == '1':
                    sql += " RIGHT JOIN ordered ON owner.show_id = ordered.show_id"
                    if classifi:
                        sql += " and ordered.user = '%s'" % classifi 
                if not status and classifi:  
                    sql += " RIGHT JOIN ordered ON owner.show_id = ordered.show_id and ordered.user = '%s'" % classifi               
                    
                sql += " WHERE owner.site_id = '2'"   
                
                if status == '2':
                    sql += " AND owner.show_id not in (select show_id from ordered)" 
                    
                if cond and content:
                    sql += " AND owner.%s like '%%%s%%'" % (cond, content)
                    
                if order == '1':
                    sql += ' ORDER BY owner.played DESC'
                elif order == '2':
                    sql += ' ORDER BY owner.fans DESC' 
                if status == '1' and not order:
                    sql += " ORDER BY ordered.ctime DESC"
                sql += ' limit %s offset %s' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
            
    def get_youtube_count(self, origin, status, cond, content, classifi):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT count(id) FROM owner "
                if status == '1':
                    sql += "RIGHT JOIN ordered ON owner.show_id = ordered.show_id "
                    if classifi:
                        sql += "and ordered.user = '%s' " % classifi 
                if not status and classifi:  
                    sql += "RIGHT JOIN ordered ON owner.show_id = ordered.show_id and ordered.user = '%s' " % classifi               
                          
                sql += "WHERE owner.site_id = '2' "
                if status == '2':
                    sql += "and owner.show_id not in (select show_id from ordered) "
                if cond and content:
                    sql += "and owner.%s like '%%%s%%' " % (cond, content)
                    
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
            
    def get_sub_showid_list(self):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT show_id, user FROM ordered "
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                        
    def get_youku(self, page, count, order, status, cond, content):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT owner.id, owner.show_id, owner.user_name, owner.intro, owner.played, owner.fans, owner.url FROM owner " 
                
                if status == '1':
                    sql += "RIGHT JOIN ordered ON owner.show_id = ordered.show_id "
                
                sql += "WHERE owner.site_id = '1' "                
                
                if status == '2':
                    sql += "and owner.show_id not in (select show_id from ordered) " 
                
                if cond and content:
                    sql += "and owner.%s like '%%%s%%' " % (cond, content)

                if order == '1':
                    sql += 'order by owner.played DESC '
                elif order == '2':
                    sql += 'order by owner.fans DESC ' 
                if status == '1' and not order:
                    sql += "ORDER BY ordered.ctime DESC "
                sql += 'limit %s offset %s' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
            
    def get_youku_count(self, origin, status,cond, content):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT count(id) FROM owner "
                if status == '1':
                    sql += "RIGHT JOIN ordered ON owner.show_id = ordered.show_id "
                sql += "WHERE owner.site_id = '1' "
                if status == '2':
                    sql += "and owner.show_id not in (select show_id from ordered) "            
                if cond and content:
                    sql += "and owner.%s like '%%%s%%' " % (cond, content)

                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_category_item(self, site_id):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT cat_id, cat_name FROM category "
                sql += " where site_id = '%s' "%site_id
                
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_keyword_list(self):
        with UgcVideoDao._instance_lock:
            try:
                sql = "SELECT kw.id, kw.keyword, kw.user, kw.site_id, kw.ext_cat_id, cg.cat_name, site.site_name FROM keyword as kw "
                sql += " left join category as cg on kw.site_id=cg.site_id and kw.ext_cat_id=cg.cat_id"
                sql += " left join site on kw.site_id=site.site_id"
                
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

