# -*- coding:utf-8 -*-
import sys
import traceback
from db_connect import MysqlConnect
from ugc_video_dao import UgcVideoDao
from ugc_audit_dao import UgcAuditDao
import threading

class DbManager(threading.Thread):

    _instance_lock = threading.Lock()
    _db_conn = None
    _daos = {}

    @staticmethod
    def instance():
        if not hasattr(DbManager, "_instance"):
            with DbManager._instance_lock:
                if not hasattr(DbManager, "_instance"):
                    DbManager._instance = DbManager()
                    DbManager._db_conn = MysqlConnect()
                    DbManager._daos.update({'ugc_video': UgcVideoDao(DbManager._db_conn), 
                                            'ugc_audit': UgcAuditDao(DbManager._db_conn), 
                                    })
        return DbManager._instance

    def commit_transaction(self):
        self._db_conn.commit()

    def get_video(self, page, count, origin, status, sort):
        with DbManager._instance_lock:
            try:
                dao = self._daos['ugc_video']
                res = dao.get_video(page, count, origin, status, sort)
                self.commit_transaction()
                return res
            except Exception, e:
                print traceback.format_exc()

    def get_video_count(self, origin, status):
        with DbManager._instance_lock:
            try:
                dao = self._daos['ugc_video']
                count = dao.get_video_count(origin, status)
                self.commit_transaction()
                return count
            except Exception, e:
                print traceback.format_exc()

    def apply_task(self, uid, tid_list):
        with DbManager._instance_lock:
            try:
                dao = self._daos['ugc_audit']
                exist = dao.apply_task(uid, tid_list)
                self.commit_transaction()
                return exist
            except Exception, e:
                print traceback.format_exc()

    def get_all_task(self):
        with DbManager._instance_lock:
            try:
                dao = self._daos['ugc_audit']
                res = dao.get_all_task()
                self.commit_transaction()
                return res
            except Exception, e:
                print traceback.format_exc()

if __name__ == "__main__":
    try:
        mgr = DbManager.instance()
        '''
        print mgr.get_video_count("upload", "unaudit")
        print mgr.apply_task('1', ['1', '2', '3'])
        print mgr.get_all_task()
        '''
        res = mgr.get_video(1, 20, '', '', '')
        if res:
            for r in res:
                print ' '.join(['%s: %s' % (k, v ) for k, v in r.items()])


    except Exception, e:
        print traceback.format_exc()
