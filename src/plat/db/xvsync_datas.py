#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from plat.settings import DATABASES_3
import traceback
import threading
import logging
logger = logging.getLogger('my')

class XVsyncDatas(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect(host=DATABASES_3['default']['HOST'],
                                    user=DATABASES_3['default']['USER'],
                                    passwd=DATABASES_3['default']['PASSWORD'],
                                    db=DATABASES_3['default']['NAME'],
                                    port=int(DATABASES_3['default']['PORT']))
        self._db_conn = db_conn

    @staticmethod
    def instance():
        if not hasattr(XVsyncDatas, "_instance"):
            with XVsyncDatas._instance_lock:
                if not hasattr(XVsyncDatas, "_instance"):
                    XVsyncDatas._instance = XVsyncDatas()
        return XVsyncDatas._instance
    
    def get_site(self):
        with XVsyncDatas._instance_lock:
            try:
                sql = "select site_id,repr from site"
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())

    def get_xvsync_list(self, page, count, channel_id, cond, content, screen):
        with XVsyncDatas._instance_lock:
            try:
                sql = "select * from cluster"
                sql += " where channel_id='%s'"%channel_id
                if screen=='1':
                    sql += " and cid in (select distinct cid from cluster_media) " 
                elif screen=='2':
                    sql += " and cid not in (select distinct cid from cluster_media)"
                
                if content:
                    sql += " and %s like '%%%s%%'"%(cond, content)
                sql += " order by release_date desc"
                sql += ' limit %s offset %s;' % (count, (int(page) - 1) * int(count))
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_xvsync_list_count(self, channel_id, cond, content, screen):
        with XVsyncDatas._instance_lock:
            try:
                sql = "select count(*) from cluster where channel_id='%s' "%channel_id 
                if screen=='1':
                    sql += " and cid in (select distinct cid from cluster_media) " 
                elif screen=='2':
                    sql += " and cid not in (select distinct cid from cluster_media)"
                    
                if content:
                    sql += " and %s like '%%%s%%'"%(cond, content)
                #print sql
                res = self._db_conn.db_fetchall(sql)
                self._db_conn.commit()
                return res[0][0]
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_xvsync_details(self, cid):#获得耦合页展示的详细信息
        with XVsyncDatas._instance_lock:
            try:
                sql = "select *, m.url from cluster as c "
                sql += " left join media as m on c.mid = m.mid " 
                sql += " where c.cid='%s' "%cid 
                
                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res[0]
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_mid_site(self, mid):#获得耦合媒体的mid
        with XVsyncDatas._instance_lock:
            try:
                sql = "select mid, site_id from cluster_media where cid='%s' "%mid

                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
              
    def get_xvsync_movie(self, mid):#获得电影耦合页的直接播放的URL
        with XVsyncDatas._instance_lock:
            try:
                sql = "SELECT url FROM play_url AS p LEFT JOIN video AS v ON v.vid=p.vid WHERE v.mid='%s'"%mid
                sql += " and p.invalid=0 and p.os_id=1"

                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                #print res
                return res[0]
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_xvsync_tv(self, mid):#获得电视剧、动漫耦合页的直接播放的URL
        with XVsyncDatas._instance_lock:
            try:
                sql = "SELECT p.url, v.vnum, v.title FROM play_url AS p LEFT JOIN video AS v ON v.vid=p.vid WHERE v.mid='%s'"%mid
                sql += " and p.invalid=0 and p.os_id=1"
                sql += " order by CAST(v.vnum AS UNSIGNED)"

                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def get_xvsync_variaty(self, mid):#获得综艺耦合页的直接播放的URL，与上一个函数排序方式不一样
        with XVsyncDatas._instance_lock:
            try:
                sql = "SELECT p.url, v.vnum, v.title FROM play_url AS p LEFT JOIN video AS v ON v.vid=p.vid WHERE v.mid='%s'"%mid
                sql += " and p.invalid=0 and p.os_id=1"
                sql += " order by v.vnum desc"

                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                
    def del_xvsync(self, mid_1, mid_2):
        with XVsyncDatas._instance_lock:
            try:
                sql = "delete from cluster_media where cid='%s' and mid='%s'"%(mid_1, mid_2)

                #print sql
                res = self._db_conn.db_fetchall(sql, as_dic=True)
                self._db_conn.commit()
                return res
            except Exception, e:
                logger.error(traceback.format_exc())
                