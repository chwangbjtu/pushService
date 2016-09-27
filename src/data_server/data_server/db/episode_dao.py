# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
from tornado import log
import traceback

class EpisodeDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._episode_tb_name = 'episode'
        self._customer_episode_tb_name = 'customer_episode'
        self._site_tb_name = 'site'
        self._ordered_tb_name = 'ordered'
        self._episode_status_tb_name = 'episode_status'
        self._step_tb_name = 'step'

    def insert_customer_episode(self, value_dict):
        try:
            keys = value_dict.keys()
            values = value_dict.values()
            sql = "INSERT INTO %s (%s, create_time, update_time) VALUES (%s, now(), now())" % (
                    self._customer_episode_tb_name, 
                    ",".join(keys),
                    ",".join(['%s'] * len(keys)))
            para = values
            if self._db_conn.execute_sql(sql, para):
                self._db_conn.commit()
                return True
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)
            return False

    def get_uid(self, user):
        try:
            sql = "SELECT id FROM auth_user WHERE username = %s" 
            para = [user,]
            res = self._db_conn.db_fetchall(sql, para)
            self._db_conn.commit()

            if res:
                return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)
    
    def get_site_id(self, user):
        try:
            sql = "SELECT site_id FROM site WHERE site_name = %s" 
            para = [user,]
            res = self._db_conn.db_fetchall(sql, para)
            self._db_conn.commit()

            if res:
                return res[0][0]
        except Exception, e:
            log.app_log.error(traceback.format_exc(), level=log.ERROR)
    
    def get_episode(self, show_id, origin=0):
        try:
            tb_name = self._episode_tb_name
            if int(origin) == 1:
                sql = "SELECT e.id, e.show_id, e.type, e.url, e.priority, e.title, e.category, e.tag, e.description, c.site_name, c.site_code FROM %s AS e \
                        LEFT JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.show_id = %%s" % \
                        (self._customer_episode_tb_name, self._site_tb_name, )
            else:
                sql = "SELECT e.id, e.show_id, e.url, e.priority,e.title, e.category, e.tag, e.description, c.site_name, c.site_code FROM %s AS e \
                        LEFT JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.show_id = %%s" % \
                        (self._customer_episode_tb_name, self._site_tb_name, )
            para = [show_id,]
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()

            if res:
                return res[0]
        except Exception, e:
            log.app_log.error("Get episode exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))
    
    #episodes that should be sent to download
    def get_recent_episodes(self, since_time, stash=None, origin=0):
        try:
            if int(origin) == 0:
                #get format above normal
                sql = "SELECT e.id, e.show_id, e.url, e.priority,e.title, e.category, e.tag, e.description, c.site_name, c.site_code FROM %s AS e \
                        LEFT JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.create_time > %%s AND e.send = 0 and (e.format_id > 1 or e.site_id = 2) " % \
                        (self._episode_tb_name, self._site_tb_name, )
            else:
                sql = "SELECT e.id, e.show_id, e.type, e.url, e.priority,e.title, e.category, e.tag, e.description, c.site_name, c.site_code FROM %s AS e \
                        LEFT JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.create_time > %%s AND e.send = 0 " % \
                        (self._customer_episode_tb_name, self._site_tb_name, )

            para = [since_time,]
            #log.app_log.debug("sql: %s para: %s" % (sql, para))
            if stash != None:
                sql += ' and e.stash = %s'
                para.append(str(stash))
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()
            return res
        except Exception, e:
            log.app_log.error("Get recent episodes exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

    def set_send(self, eid, origin=0):
        try:
            tb_name = self._episode_tb_name
            if int(origin) == 1:
                tb_name = self._customer_episode_tb_name

            sql = "UPDATE %s SET send = 1 WHERE id = %%s " % (tb_name, )
            para = (eid, )
            #log.app_log.debug("sql: %s para: %s" % (sql, para))
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()

        except Exception, e:
            log.app_log.error("Get recent episodes exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

    def set_control_info(self,dpara,origin=0):
        try:
            para = []
            tb_name = self._episode_tb_name
            if int(origin) == 1:
                tb_name = self._customer_episode_tb_name

            tsql = "update %s set send = 1 "
            #if audit or len(audit) != 0:
            if 'audit' in dpara and str(dpara['audit']) == '0':
                tsql += ",audit = 0 "

            if 'priority' in dpara:
                if len(tsql) != 0:
                    tsql += ",priority = %%s "
                else:
                    tsql = "update %s set send = 1, priority = %%s "
                para.insert(0,dpara['priority'])
            tsql += " where id = %%s "
            tlen = len(para)
            para.insert(tlen,str(dpara['id']))
            sql = tsql % (tb_name,)
            self._db_conn.execute_sql(sql, para)
            self._db_conn.commit()
        except Exception, e:
            log.app_log.error("set_control_info exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))
    
    #episodes that should be sent to maze
    def get_maze_episodes(self, since_time, origin=0):
        try:
            #spider episode
            if int(origin) == 0:
                sql = "SELECT s.id, s.url, s.origin, e.show_id, e.title, e.category, e.tag, e.description, e.priority, e.audit, e.played, e.duration, e.upload_time, \
                        c.site_name, c.site_code FROM %s AS s \
                        JOIN %s AS e ON e.id = s.eid \
                        JOIN %s AS p ON p.step_id = s.step_id \
                        JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.create_time > %%s and p.step_name = 'download' and s.status = '1' and s.send = 0 and s.origin = %s " % \
                        (self._episode_status_tb_name, self._episode_tb_name, self._step_tb_name, self._site_tb_name, origin)
            #customer episode
            else:
                sql = "SELECT s.id, s.url, s.origin, e.show_id, e.title, e.category, e.tag, e.description, e.priority, e.audit, e.type, \
                        c.site_name, c.site_code FROM %s AS s \
                        JOIN %s AS e ON e.id = s.eid \
                        JOIN %s AS p ON p.step_id = s.step_id \
                        JOIN %s AS c ON e.site_id = c.site_id \
                        WHERE e.create_time > %%s and p.step_name = 'download' and s.status = '1' and s.send = 0 and s.origin = %s " % \
                        (self._episode_status_tb_name, self._customer_episode_tb_name, self._step_tb_name, self._site_tb_name, origin)

            para = [since_time,]
            #log.app_log.debug("sql: %s para: %s" % (sql, para))
            res = self._db_conn.db_fetchall(sql, para, as_dic=True)
            self._db_conn.commit()
            return res
        except Exception, e:
            log.app_log.error("Get recent episodes exception: %s " % traceback.format_exc())
            log.app_log.debug("sql: %s para: %s" % (sql, para))

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        episode_dao = EpisodeDao(db_conn)
        print episode_dao.get_site_id('kuaikan')
        '''
        customer_episode = {'uid': '18', 'type': 1, 'show_id': '111111', 'site_id': 9, 'priority': 2, 'audit': 0, 'title': u'测试一个', 'category': u'快看', 'tag': u'搞笑|奇趣', 'url': 'http://v.youku.com/v_show/id_XNzkxMDE4Mjky_ev_1.html', 'description': u'测试'}
        episode_dao.insert_customer_episode(customer_episode)
        '''

        '''
        res = episode_dao.get_episode('ZxcaK3Y_rBM', origin=1)
        if res:
            log.app_log.debug(' '.join(['%s: %s' % (k, v ) for k, v in res.items()]))
        db_conn.commit()
        '''
        '''
        res = episode_dao.get_recent_episodes('2014-11-28 14:00', stash=0, origin=0)
        if res:
            for r in res:
                #log.app_log.debug('episode: %s %s, %s, %s' % (r['show_id'], r['title'], r['update_time'], r['create_time']))
                log.app_log.debug(' '.join(['%s: %s' % (k, v ) for k, v in r.items()]))
        db_conn.commit()
        '''
        '''
        '''
        '''
        episode_dao.set_send('1507392', 0)
        '''
        '''
        res = episode_dao.get_maze_episodes('2014-11-28 14:00', origin=0)
        if res:
            for r in res:
                log.app_log.debug(' '.join(['%s: %s' % (k, v ) for k, v in r.items()]))
        db_conn.commit()
        '''

    except Exception,e:
        log.app_log.error(traceback.format_exc())
