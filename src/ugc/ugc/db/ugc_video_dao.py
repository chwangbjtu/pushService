# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
import traceback

class UgcVideoDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._video_tb_name = 'ugc_video'
        self._user_tb_name = 'auth_user'

    def status_filter(self, status):
        cond = ""
        if status == "unaudit":
            cond = ' and step = "audit" and status = 0 '
        elif status == "pass":
            cond = ' and (step = "mpacker" or step = "distribute") '
        elif status == "unpass":
            cond = ' and step = "audit" and status = 2 '
        elif status == "untrans":
            cond = ' and step = "transcode" and status = 0 '
        elif status == "fail":
            cond = ' and (step = "transcode" or step = "mpacker" or step = "distribute") and status = 2 '
        else:
            cond = ' '
        return cond

    def origin_filter(self, origin):
        cond = ""
        if origin == "upload":
            cond = ' and origin = "upload" and uid != 9 '
        elif origin == "forwards":
            cond = ' and origin = "forwards" '
        elif origin == "youku":
            cond = ' and origin = "spider" and site = "yk" '
        elif origin == "youtube":
            cond = ' and origin = "upload" and uid = 9 '
        else:
            cond = ' '
        return cond

    def sort_filter(self, sort):
        cond = ""
        if sort == "pub_time":
            cond = ' order by pub_time desc '
        elif sort == "ctime":
            cond = ' order by ctime desc '
        elif sort == "mtime":
            cond = ' order by mtime desc '
        elif sort == "priority":
            cond = ' order by priority desc '
        else:
            cond = ' order by priority desc '
        return cond

    def get_video(self, page, count, origin, status, sort):
        try:
            sql = "SELECT v.tid, v.uid, v.title, v.tags, v.channel, v.priority, v.pub_time, v.ctime, v.mtime, v.site, v.origin, v.step, v.status, u.username FROM %s AS v JOIN %s AS u ON v.uid = u.id WHERE true " % (self._video_tb_name, self._user_tb_name)
            para = []
            
            #status
            if status:
                sql += self.status_filter(status)

            #origin
            if origin:
                sql += self.origin_filter(origin)

            #sort
            if sort:
                sql += self.sort_filter(sort)

            sql += ' limit %s offset %s ' % (count, (int(page) - 1) * int(count))

            print sql
            res = self._db_conn.db_fetchall(sql, as_dic=True)
            return res
        except Exception, e:
            print "Get video exception: %s " % traceback.format_exc()
            print "sql: %s para: %s" % (sql, para)

    def get_video_count(self, origin, status):
        try:
            sql = "SELECT count(tid) FROM %s WHERE true " % (self._video_tb_name, )
            para = []

            #origin
            if origin:
                sql += self.origin_filter(origin)

            #status
            if status:
                sql += self.status_filter(status)

            print sql
            res = self._db_conn.db_fetchall(sql)
            return res[0][0]
        except Exception, e:
            print "Get video exception: %s " % traceback.format_exc()
            print "sql: %s para: %s" % (sql, para)

    
if __name__ == "__main__":

    try:
        ugc_video_dao = UgcVideoDao()

        res = ugc_video_dao.get_video(1, 20, '', '', '')
        print res
        if res:
            for r in res:
                print ' '.join(['%s: %s' % (k, v ) for k, v in r.items()])
        '''

        res = ugc_video_dao.get_video_count('', '')
        if res:
            print 'video count: %s' % (res,)
        '''


    except Exception,e:
        print traceback.format_exc()
