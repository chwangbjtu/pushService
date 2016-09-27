#!/usr/bin/python
# -*- coding:utf-8 -*-

#store ip:port/api/?cmd=upload_data&cli=upload_verify_data report data.
import json
import verify_ms_info
import constant
import threading
import db_mgr
import log
import etc

class VerifyMsInfoMgr(threading.Thread):
    _instance_lock = threading.Lock()

    def  __init__(self):
        self._audit_data = verify_ms_info.VerifyMsInfo()
        self._log_info = log.MakeLog(etc.log_for_process)
        self._log_error = log.MakeLog(etc.error_for_process)
        self._log_info.start()
        self._log_error.start()
        self._db_inst  = db_mgr.DatabaseManager.instance()

    @staticmethod
    def instance():
        if not hasattr(VerifyMsInfoMgr, "_instance"):
            with VerifyMsInfoMgr._instance_lock:
                if not hasattr(VerifyMsInfoMgr, "_instance"):
                    VerifyMsInfoMgr._instance = VerifyMsInfoMgr()
        return VerifyMsInfoMgr._instance

    def process(self, verify_ms_json):
        try:
            ms_info =  verify_ms_info.VerifyMsInfo()
            ret_flag = ms_info.serialization(verify_ms_json)
            if ret_flag == False:
                reason = 'VerifyMsInfoMgr::serialization error.'
                return (constant.FAIL ,reason)
            (code, res) = self._db_inst.db_verify_mserver_info(ms_info)
            if code != constant.SUCCESS:
                reason = 'VerifyDataMgr::db_verify_infohash error.'
                return (constant.FAIL ,reason)
            return (constant.SUCCESS, res)
        except Exception,e:
            reason = "has exception in VerifyMsInfoMgr::process with %s" % str(e)
            return (constant.FAIL ,reason)