#!/bin/env python
# -*- coding: utf-8    -*- 

import MySQLdb
import db_procedure
import constant
import etc
import threading
import log
import verify_data_st
import verify_infohash
import verify_ms_info

class DatabaseManager(threading.Thread):
    _instance_lock = threading.Lock()

    def __init__(self):
        self.__conn = MySQLdb.connect(host=etc.host, user=etc.user, passwd=etc.passwd,db=etc.db, charset = 'utf8')
        self._procedure = db_procedure.db_procedure(self.__conn)
        self._log_info = log.MakeLog(etc.log_for_db_manager)
        self._log_error = log.MakeLog(etc.error_for_db_manager)
        self._log_info.start()
        self._log_error.start()

    @staticmethod
    def instance():
        if not hasattr(DatabaseManager, "_instance"):
            with DatabaseManager._instance_lock:
                if not hasattr(DatabaseManager, "_instance"):
                    DatabaseManager._instance = DatabaseManager()
        return DatabaseManager._instance

    def close(self):
         self._procedure.close()

    #请求审核接口  ip:port/api/?cmd=upload_data&cli=upload_verify_data
    def db_verify_data(self, audit_verify_data):
          try:
             v_tid = audit_verify_data.tid
             v_state = audit_verify_data.state
             v_ip = audit_verify_data.ip
             v_port = audit_verify_data.port
             
             if v_tid == "" or v_state == "" or v_ip == "" or v_port == "":
                reason = 'the value of the db_verify_data is null'
                return (constant.FAIL, reason)
             (code, res) = self._procedure.call_proc_verify_data_base(v_tid, v_state, v_ip, v_port)
             if code != constant.SUCCESS:
                 reason = 'call_proc_verify_data_base error.'
                 return (constant.FAIL, reason)

             #funshion file process
             ret_call = self._procedure.call_proc_verify_funshion_mgr(audit_verify_data)
             if ret_call == constant.FAIL:
                resean = "there has exception in call_proc_verify_funshion_file"
                self._log_info.logerror(resean)
                return (constant.FAIL, resean)
             elif ret_call == constant.NOEXISTS:
                resean = "there has no record to call_proc_verify_funshion_file. %s"  % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, resean)
             else:
                resean = "ok"
                info_str = "db_verify_data :%s" % (resean)
                self._log_info.loginfo("call_proc_verify_funshion_file  " + info_str)
                return (constant.SUCCESS, resean)
          except Exception, e:
              resean = "there has exception in db_verify_data with  error: %s"  % (str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)

    #请求分发接口  ip:port/api/?cmd=upload_hash_data&cli=upload_verify_hash
    def db_verify_infohash(self, verify_infohash):
        try:
             (code, res) = self._procedure.call_proc_verify_infohash(verify_infohash)
             if code != constant.SUCCESS:
                 reason = 'call_proc_verify_data_base error.'
                 return (constant.FAIL, reason)
             return (constant.SUCCESS, res)
        except Exception, e:
              resean = "there has exception in db_verify_infohash with  error: %s"  % (str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)
    
    def db_verify_mserver_info(self, ms_info):
        try:
             dat_infohash = ms_info.dat_infohash
             dat_size = ms_info.dat_size
             mserver_ip = ms_info.ms_server_ip
             mserver_port = ms_info.ms_server_port
             
             (code, res) = self._procedure.call_proc_verify_mserver_info(dat_infohash, dat_size, mserver_ip, mserver_port)
             if code != constant.SUCCESS:
                 reason = 'call_proc_verify_data_base error.'
                 return (constant.FAIL, reason)
             return (constant.SUCCESS, res)
        except Exception, e:
              resean = "there has exception in db_verify_infohash with  error: %s"  % (str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)
      
   




