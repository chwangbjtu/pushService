#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import verify_infohash
import constant
import threading
import db_mgr


class VerifyInfohashMgr(threading.Thread):
    _instance_lock = threading.Lock()

    def  __init__(self):
        self._infohash = verify_infohash.VerifyInfoHash()
        self._db_inst  = db_mgr.DatabaseManager.instance()

    @staticmethod
    def instance():
        if not hasattr(VerifyInfohashMgr, "_instance"):
            with VerifyInfohashMgr._instance_lock:
                if not hasattr(VerifyInfohashMgr, "_instance"):
                    VerifyInfohashMgr._instance = VerifyInfohashMgr()
        return VerifyInfohashMgr._instance

    def process(self, infohash_json):
        try:
            #json_str = json.loads(infohash_json)
            audit_infohash = verify_infohash.VerifyInfoHash()
            ret_flag = audit_infohash.serialization(infohash_json)
            if ret_flag == False:
                reason = 'VerifyDataMgr::serialization error.'
                return (constant.FAIL ,reason)
            (code, res) = self._db_inst.db_verify_infohash(audit_infohash)
            if code != constant.SUCCESS:
                reason = 'VerifyDataMgr::db_verify_infohash error.'
                return (constant.FAIL ,reason)
            return (constant.SUCCESS, res)
        except Exception,e:
            print e
            reason = "has exception in VerifyDataMgr::process with %s" % str(e)
            return (constant.FAIL ,reason)