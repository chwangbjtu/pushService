# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from plat.settings import DATABASES_2
import traceback
import threading
import logging
logger = logging.getLogger('my')

class DBDatas(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect(host=DATABASES_2['default']['HOST'],
                                    user=DATABASES_2['default']['USER'],
                                    passwd=DATABASES_2['default']['PASSWORD'],
                                    db=DATABASES_2['default']['NAME'],
                                    port=int(DATABASES_2['default']['PORT']))
        self._db_conn = db_conn

    @staticmethod
    def instance():
        if not hasattr(DBDatas, "_instance"):
            with DBDatas._instance_lock:
                if not hasattr(DBDatas, "_instance"):
                    DBDatas._instance = DBDatas()
        return DBDatas._instance
            
    def get_douban_video(self, page, count, classifi, order, cond, content):
        with DBDatas._instance_lock:
            try:
                sql = "SELECT cat_id,score,title,aka,director,actor,district,type,language,mainpic,url FROM douban "
                sql += " where true "
                 
                if cond and content:
                    if cond == "title":
                        sql += " AND title LIKE '%%%s%%' or aka LIKE '%%%s%%'" % (content,content)
                    if cond == "type":
                        sql += " AND type LIKE '%%%s%%'" % content
                         
                if classifi: 
                    sql += " AND cat_id = '%s'" %(classifi)
                     
                if order:
                    sql += " order by %s desc " %(order)
     
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_douban_video_count(self, classifi, cond, content):
        with DBDatas._instance_lock:
            try:
                sql = "SELECT count(id) FROM douban "
                sql += " WHERE true "
                
                if classifi: 
                    sql += " AND cat_id = '%s'" %(classifi)
                 
                if cond and content:
                    if cond == "title":
                        sql += " AND title LIKE '%%%s%%' or aka LIKE '%%%s%%'" % (content,content)
                    if cond == "type":
                        sql += " AND type LIKE '%%%s%%'" % content
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
                
    def get_FunDB_video(self, page, count, disable, status, order, cond, content):
        with DBDatas._instance_lock:
            try:
                '''
                sql = "SELECT fd.*,f.name,f.category,f.director,f.actor,f.disable,d.show_id,d.title,d.director as db_dir,d.actor as db_act FROM fun_dou_rel AS fd"
                sql += " LEFT JOIN funshion AS f ON f.media_id=fd.fun_id"
                sql += " LEFT JOIN douban AS d ON d.show_id=fd.dou_id"
                sql += " WHERE true "
                '''

                sql = "SELECT fd.id,fd.status,fd.fit,f.media_id, f.name,f.category,f.director,f.actor,f.disable,d.show_id,d.title,d.director as db_dir,d.actor as db_act,d.type FROM funshion AS f \
                        LEFT join fun_dou_rel AS fd ON fd.fun_id = f.media_id \
                        LEFT join douban AS d ON fd.dou_id = d.show_id \
                        WHERE true "
                 
                if cond and content:
                    if cond == "title":
                        sql += " AND d.title LIKE '%%%s%%'" % (content)
                    if cond == "name":
                        sql += " AND f.name LIKE '%%%s%%'" % (content)
                    if cond == "category":
                        sql += " AND f.category LIKE '%%%s%%'" % (content)
                          
                if disable: 
                    sql += " AND f.disable = '%s'" %(disable)
                      
                if status:
                    sql += " AND fd.status = '%s' " %(status)
                    
                if order == 0:
                    sql += " order by fd.fit desc "
                    
                #sql += " group by fd.fun_id having max(fd.fit)"
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_FunDB_video_count(self, disable, status, cond, content):
        with DBDatas._instance_lock:
            try:
                '''
                sql = "SELECT count(distinct fd.fun_id) FROM fun_dou_rel as fd "
                sql += " LEFT JOIN funshion AS f ON f.media_id=fd.fun_id"
                sql += " LEFT JOIN douban AS d ON d.show_id=fd.dou_id"
                sql += " WHERE true "
                '''

                sql = "SELECT count(*) FROM funshion AS f \
                        LEFT join fun_dou_rel AS fd ON fd.fun_id = f.media_id \
                        LEFT join douban AS d ON fd.dou_id = d.show_id \
                        WHERE true "
                 
                
                if status:
                    sql += " AND fd.status = '%s' " %(status)
                    
                if disable: 
                    sql += " AND f.disable = '%s'" %(disable)
                  
                if cond and content:
                    if cond == "title":
                        sql += " AND d.title LIKE '%%%s%%'" % (content)
                    if cond == "name":
                        sql += " AND f.name LIKE '%%%s%%'" % (content)
                    if cond == "category":
                        sql += " AND f.category LIKE '%%%s%%'" % (content)
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                return 0
                
    def update_fun_db(self, id, media_id, name, director,actor,category):
        with DBDatas._instance_lock:
            try:
                sql = "update funshion f inner join fun_dou_rel fd on f.media_id=fd.fun_id"
                sql += " set f.name='%s', f.director='%s', f.actor='%s', fd.status=1, f.category='%s'"%(name,director,actor,category)
                sql += " where fd.id='%s' "%(id)
                #print sql
                res = self._db_conn.execute_sql(sql)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def eliminate_fun_db(self, id):
        with DBDatas._instance_lock:
            try:
                sql = "update fun_dou_rel set status=2 where id='%s' "%(id)
                #print sql
                res = self._db_conn.execute_sql(sql)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_funid_video(self,id,media_id):
        with DBDatas._instance_lock:
            try:
                sql = "SELECT fd.*,f.name,f.category,f.director,f.actor,f.disable,d.show_id,d.title,d.director as db_dir,d.actor as db_act FROM fun_dou_rel AS fd"
                sql += " LEFT JOIN funshion AS f ON f.media_id=fd.fun_id"
                sql += " LEFT JOIN douban AS d ON d.show_id=fd.dou_id"
                sql += " WHERE fd.fun_id=%s and fd.id!=%s "%(media_id,id)
                res = self._db_conn.db_fetchall(sql,as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_douban_detail(self, dou_id):
        with DBDatas._instance_lock:
            try:
                all_info = {'title': [], 'director': [], 'actor': [], 'type': ''}

                #title
                sql = "SELECT title FROM douban_title_index WHERE show_id = %s" % dou_id
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                if res:
                    all_info['title'] = [r['title'] for r in res]

                #director
                sql = "SELECT director FROM douban_director_index WHERE show_id = %s" % dou_id
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                if res:
                    all_info['director'] = [r['director'] for r in res]

                #actor
                sql = "SELECT actor FROM douban_actor_index WHERE show_id = %s" % dou_id
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                if res:
                    all_info['actor'] = [r['actor'] for r in res]

                #other info
                sql = "SELECT show_id, type, district, release_date, language, runtime FROM douban WHERE show_id = %s LIMIT 1" % dou_id
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                if res:
                    all_info.update(res[0])
                
                return all_info

            except Exception, e:
                logger.error(traceback.format_exc())

    def update_funshion_detail(self, fun_id, title=None, director=None, actor=None, category=None):
        with DBDatas._instance_lock:
            try:
                sql = "UPDATE funshion SET "
                para = []
                if title:
                    sql += " name = %s, "
                    para.append(title[0])
                if director:
                    sql += " director = %s, "
                    para.append(",".join(director))
                if actor:
                    sql += " actor = %s, "
                    para.append(",".join(actor))
                if category:
                    sql += " category = %s "
                    para.append(category)
                sql += " WHERE media_id = %s"
                para.append(fun_id)

                self._db_conn.execute_sql(sql, para)
                self._db_conn.commit()
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_funshion_detail(self, fun_id):
        with DBDatas._instance_lock:
            try:
                all_info = {}

                sql = "SELECT media_id, name, director, actor, category, release_date FROM funshion WHERE media_id = %s LIMIT 1" % fun_id
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                if res:
                    all_info.update(res[0])
                
                return all_info

            except Exception, e:
                logger.error(traceback.format_exc())

    def update_fun_dou_fit(self, fun_id, dou_id, fit):
        with DBDatas._instance_lock:
            try:
                sql = "UPDATE fun_dou_rel SET fit = %s, status = 1 WHERE fun_id = %s AND dou_id = %s"
                sql2 = "UPDATE fun_dou_rel SET status = 2 WHERE fun_id = %s AND dou_id != %s"
                para = [fit, fun_id, dou_id]
                para2 = [fun_id, dou_id]

                self._db_conn.execute_sql(sql, para)
                self._db_conn.execute_sql(sql2, para2)
                self._db_conn.commit()
            except Exception, e:
                logger.error(traceback.format_exc())
