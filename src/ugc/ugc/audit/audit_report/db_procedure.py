#!/bin/env python
# -*- coding: utf-8    -*- 
import etc
import log
import json
import constant
import verify_data_st
import verify_infohash
import verify_ms_info

class db_procedure:
  
    def __init__(self, conn):
        self.__conn = conn                                                                            
        self.__proc_info = log.MakeLog(etc.log_for_procedure)
        self.__proc_error = log.MakeLog(etc.error_for_procedure)
        self.__proc_info.start()
        self.__proc_error.start()

    def close(self):
        if (self.__conn == True):
            self.__conn.close()

    def call_proc_verify_data_base(self, tid, state, ip, port):
        try:
            connstr = "call proc_verify_video_base('%s', '%s', '%s', '%s')" % (tid, state, ip, port)
            print connstr
            cursor = self.__conn.cursor()
            cursor.execute(connstr)
            db_records=cursor.fetchall()
            cursor.close()
            if not db_records:
                resean =  'no record.'
                return (constant.NOT_EXISTS, None)
            else:
                ret_flag = None
                for rec in db_records:
                    ret_flag = rec[0]
                print 'call_proc_verify_data_base ok', ret_flag
                return (constant.SUCCESS, ret_flag)
        except Exception, e:
            errinfo = "there has exception in call_proc_verify_data_base with  %s" % (str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, errinfo)


    def call_proc_verify_funshion_mgr(self, audit_verify_data):
        try:
            tid = audit_verify_data.tid
            state = audit_verify_data.state
            if state == 'success':
                for key in audit_verify_data.funshion_list:
                    funshion = audit_verify_data.funshion_list[key]
                    code = self.call_proc_verify_funshion_file(tid, funshion.funshion_id, funshion.rate, funshion.small_image, funshion.large_image, funshion.video_url,
                                                        funshion.filename, funshion.filesize, funshion.milliseconds)
                    if code != constant.SUCCESS:
                        reason =  'call_proc_verify_funshion_file has error.'
                        return (constant.FAIL, reason)
                return (constant.SUCCESS,state)
            else:
                print 'state: fail'
                return (constant.SUCCESS, state)
        except Exception, e:
            errinfo = "there has exception in call_proc_verify_funshion_mgr with %s" % (str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, errinfo)


    #更新funshion视频信息
    def call_proc_verify_funshion_file(self, tid, funshion_id, rate, small_image, large_image, video_url, filename, size, milliseconds):
        try:
            print type(long(size)), type(long(milliseconds))
            connstr = "call proc_verify_file('%s','%s', '%s', '%s', '%s', '%s', '%s', %ld, %ld)" % (tid, funshion_id, rate, small_image, large_image, video_url, filename, long(size), long(milliseconds))
            print connstr
            cursor = self.__conn.cursor()
            cursor.execute(connstr)
            db_records=cursor.fetchall()
            cursor.close()
            if not db_records:
                print 'no record.'
                return constant.NOT_EXISTS
            else:
                ret_flag = None
                #print 'return: ', db_records
                for rec in db_records:
                    ret_flag = rec[0]
                    
                print 'call_proc_verify_funshion_file ok, ', ret_flag
                return constant.SUCCESS
        except Exception, e:
            errinfo = "there has exception in call_proc_verify_funshion_file with%s" % (str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  constant.FAIL

     #请求分发接口
    def call_proc_verify_infohash(self, verify_infohash):
        try:
            infohash = verify_infohash.info_hash
            file_list = verify_infohash.file_list
            for file in file_list:
                connstr = "call proc_verify_infohash('%s','%s', '%s')" % (infohash, file.funshion_id, file.tid)
                print connstr
                cursor = self.__conn.cursor()
                cursor.execute(connstr)
                db_records=cursor.fetchall()
                cursor.close()
                if not db_records:
                    resean =  'no record.'
                    return (constant.NOT_EXISTS,resean)
                else:
                   ret_flag = None
                   for rec in db_records:
                        ret_flag = rec[0]
                        infohash = rec[1]
                   print 'call_proc_verify_funshion_file ok, ', ret_flag
                   return (constant.SUCCESS,infohash)
        except Exception, e:
            errinfo = "there has exception in call_proc_verify_infohash with  %s" % (str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, errinfo)


     #开始分发接口
    def call_proc_verify_mserver_info(self, dat_infohash, dat_size, mserver_ip, mserver_port):
        try:
            connstr = "call proc_verify_ms_dat('%s', %d, '%s', '%s')" % (dat_infohash, dat_size, mserver_ip, mserver_port)
            print connstr
            cursor = self.__conn.cursor()
            cursor.execute(connstr)
            db_records=cursor.fetchall()
            cursor.close()
            if not db_records:
                resean =  'no record.'
                return (constant.NOT_EXISTS,resean)
            else:
                ret_flag = None
                for rec in db_records:
                    ret_flag = rec[0]
                    infohash = rec[1]
                print 'call_proc_verify_funshion_file ok, ', ret_flag
                return (constant.SUCCESS,infohash)
        except Exception, e:
            errinfo = "there has exception in call_proc_verify_mserver_info with  %s" % (str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, errinfo)
   
