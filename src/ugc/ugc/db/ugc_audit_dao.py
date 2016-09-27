# -*- coding:utf-8 -*-
import sys
from db_connect import MysqlConnect
import traceback

class UgcAuditDao(object):
    def __init__(self, db_conn=None):
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._audit_workspace_tb_name = 'ugc_audit_workspace'
        self._user_tb_name = 'auth_user'

    def get_all_task(self):
        try:
            tasks = {}
            sql = "SELECT a.tid, u.username FROM %s AS a JOIN %s as u ON a.uid = u.id" % (self._audit_workspace_tb_name, self._user_tb_name)
            para = []
            print sql

            res = self._db_conn.db_fetchall(sql, )
            if res:
                for record in res:
                    tasks[record[0]] = record[1]
            return tasks

        except Exception, e:
            print "Get task exception: %s " % traceback.format_exc()
            print "sql: %s para: %s" % (sql, para)


    def get_task(self, tid):
        try:
            sql = "SELECT tid from %s where tid = %%s" % (self._audit_workspace_tb_name, )
            para = [tid, ]
            #print "[%s] [%s]" % (sql, para)

            res = self._db_conn.db_fetchall(sql, para)
            if res:
                return res[0][0]

        except Exception, e:
            print "Get task exception: %s " % traceback.format_exc()
            print "sql: %s para: %s" % (sql, para)

    def apply_task(self, uid, tid_list):
        try:
            exist = []
            for tid in tid_list:
                if self.get_task(tid):
                    exist.append(tid)
                    continue

                sql = "INSERT INTO %s (tid, uid, time) values (%%s, %%s, now())" % (self._audit_workspace_tb_name, )
                para = [tid, uid]
            
                print "[%s] [%s]" % (sql, para)
                res = self._db_conn.execute_sql(sql, para)
            return exist
        except Exception, e:
            print "Apply task exception: %s " % traceback.format_exc()
            print "sql: %s para: %s" % (sql, para)

if __name__ == "__main__":

    try:
        ugc_audit_dao = UgcAuditDao()

        '''
        tid_list = ["1", "2", "3"]
        ugc_audit_dao.apply_task('1', tid_list)
        ugc_audit_dao._db_conn.commit()
        '''

        print ugc_audit_dao.get_all_task()

    except Exception,e:
        print traceback.format_exc()
