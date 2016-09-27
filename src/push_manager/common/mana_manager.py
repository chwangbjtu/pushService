# -*- coding:utf-8 -*-
import traceback
from tornado import log

import sys
sys.path.append('.')
from conf import Conf

from db.mysql_connect import MysqlConnect
from db.fs_msg_pool_dao import FsMsgPoolDao
from db.fs_msg_info_dao import FsMsgInfoDao
from db.fs_msg_push_dao import FsMsgPushDao
from db.fs_app_info_dao import FsAppInfoDao
from db.fs_cmd_info_dao import FsCmdInfoDao

class ManaManager(object):

    def __init__(self):
        self._mysql = MysqlConnect(host=Conf.sql_host, port=Conf.sql_port, user=Conf.sql_user, passwd=Conf.sql_passwd, db=Conf.sql_db)
        self._daos = {'fs_msg_pool':FsMsgPoolDao(self._mysql),
                      'fs_msg_info':FsMsgInfoDao(self._mysql),
                      'fs_msg_push':FsMsgPushDao(self._mysql),
                      'fs_app_info':FsAppInfoDao(self._mysql),
                      'fs_cmd_info':FsCmdInfoDao(self._mysql)}

    def commit_transaction(self):
        try:
            self._mysql.commit()
        except Exception, e:
            self.rollback()
            log.app_log.error(traceback.format_exc())

    def rollback_transaction(self):
        try:
            self._mysql.rollback()
        except Exception, e:
            log.app_log.error(traceback.format_exc())


    #----------------fs_msg_pool------------
    def insert_fs_msg_pool(self, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_pool']
            res = dao.insert(dict_data)
            if commit:
                self.commit_transaction()
            if res:
                res = self._mysql.insert_id()
                return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def update_fs_msg_pool(self, msg_id, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_pool']
            res = dao.update(msg_id, dict_data)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def delete_fs_msg_pool(self, msg_id, commit=False):
        try:
            dao = self._daos['fs_msg_pool']
            res = dao.delete(msg_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_fs_msg_pool(self, msg_id, commit=False): 
        try:
            dao = self._daos['fs_msg_pool']
            res = dao.query(msg_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())


    #----------------fs_msg_info------------
    def update_insert_fs_msg_info(self, dict_data, commit=False):
        try:
            msg_id = dict_data['msg_id']
            res = self.query_fs_msg_info(msg_id, commit) 
            if res:
                #更新
                res = self.update_fs_msg_info(msg_id, dict_data, commit)
                if res is not None:
                    res = msg_id
            else:
                #插入
                res = self.insert_fs_msg_info(dict_data, commit)
                if res:
                    res = self._mysql.insert_id()
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def insert_fs_msg_info(self, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_info']
            res = dao.insert(dict_data)
            if commit:
                self.commit_transaction()
            if res:
                res = self._mysql.insert_id()
                return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def update_fs_msg_info(self, msg_id, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_info']
            res = dao.update(msg_id, dict_data)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def delete_fs_msg_info(self, msg_id, commit=False):
        try:
            dao = self._daos['fs_msg_info']
            res = dao.delete(msg_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_fs_msg_info(self, msg_id, commit=False): 
        try:
            dao = self._daos['fs_msg_info']
            res = dao.query(msg_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())


    #----------------fs_msg_push------------
    def update_insert_fs_msg_push(self, dict_data, commit=False):
        try:
            msg_id = dict_data['msg_id']
            app_id = dict_data['app_id']
            res = self.query_fs_msg_push_by_msgid_appid(msg_id, app_id, commit) 
            if res:
                #更新
                push_id = res[0]['push_id']
                res = self.update_fs_msg_push_by_msgid_appid(msg_id, app_id, dict_data, commit)
                if res is not None:
                    res = push_id
            else:
                #插入
                res = self.insert_fs_msg_push(dict_data, commit)
                if res:
                    res = self._mysql.insert_id()
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def insert_fs_msg_push(self, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.insert(dict_data)
            if commit:
                self.commit_transaction()
            if res:
                res = self._mysql.insert_id()
                return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def update_fs_msg_push(self, push_id, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.update(push_id, dict_data)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def delete_fs_msg_push(self, push_id, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.delete(push_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def update_fs_msg_push_by_msgid_appid(self, msg_id, app_id, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.update_by_msgid_appid(msg_id, app_id, dict_data)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def update_fs_msg_push_by_msgid(self, msg_id, dict_data, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.update_by_msgid(msg_id, dict_data)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_fs_msg_push(self, push_id, commit=False): 
        try:
            dao = self._daos['fs_msg_push']
            res = dao.query(push_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_fs_msg_push_by_msgid_appid(self, msg_id, app_id, commit=False): 
        try:
            dao = self._daos['fs_msg_push']
            res = dao.query_by_msgid_appid(msg_id, app_id)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def get_maxid_fs_msg_push(self, commit=False):
        try:
            dao = self._daos['fs_msg_push']
            res = dao.get_maxid()
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())


    #----------------fs_app_info------------
    def query_fs_app_info(self, commit=False):
        try:
            dao = self._daos['fs_app_info']
            res = dao.query()
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_field_by_app_name_fs_app_info(self, app_name, field, commit=False): 
        try:
            dao = self._daos['fs_app_info']
            res = dao.query_field_by_app_name(app_name, field)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

    def query_by_app_name_fs_app_info(self, app_name, commit=False): 
        try:
            dao = self._daos['fs_app_info']
            res = dao.query_by_app_name(app_name)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())


    #----------------fs_cmd_info------------
    def query_field_fs_cmd_info(self, cmd_id, field, commit=False): 
        try:
            dao = self._daos['fs_cmd_info']
            res = dao.query_field(cmd_id, field)
            if commit:
                self.commit_transaction()
            return res
        except Exception, e:
            self.rollback_transaction()
            log.app_log.error(traceback.format_exc())

if __name__ == '__main__':
    test = ManaManager()
    dict = {'push_state':'dismissed'}
    res = test.update_fs_msg_push_by_msgid_appid('1670','38',dict)
    print res
