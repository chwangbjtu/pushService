#!/usr/bin/python
# -*- coding:utf-8 -*-

#store ip:port/api/?cmd=upload_data&cli=upload_verify_data report data.
import json
import verify_data_st
import constant
import threading
import db_mgr
import log
import etc

class VerifyDataMgr(threading.Thread):
    _instance_lock = threading.Lock()

    def  __init__(self):
        self._log_info = log.MakeLog(etc.log_for_process)
        self._log_error = log.MakeLog(etc.error_for_process)
        self._log_info.start()
        self._log_error.start()
        self._db_inst  = db_mgr.DatabaseManager.instance()

    @staticmethod
    def instance():
        if not hasattr(VerifyDataMgr, "_instance"):
            with VerifyDataMgr._instance_lock:
                if not hasattr(VerifyDataMgr, "_instance"):
                    VerifyDataMgr._instance = VerifyDataMgr()
        return VerifyDataMgr._instance

    def process(self, verify_data_json):
        try:
            audit_data = verify_data_st.AuditVerifyData()
            ret_flag = audit_data.serialization(verify_data_json)
            if ret_flag == False:
                reason = 'VerifyDataMgr::serialization error.'
                return (constant.FAIL ,reason)
            (code, res) = self._db_inst.db_verify_data(audit_data)
            if code != constant.SUCCESS:
                print code
                return (code, res)
            return (constant.SUCCESS, res)
        except Exception,e:
            print e
            reason = "has exception in VerifyDataMgr::process with %s" % str(e)
            return (constant.FAIL ,reason)
