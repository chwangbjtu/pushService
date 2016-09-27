#!/bin/env python
# -*- coding: utf-8    -*- 

import MySQLdb
import db_procedure
import constant
import etc
import threading
import log
import json
import http_client
import pytools
import task_queue
import send_thread

class DatabaseManager(threading.Thread):
    _instance_lock = threading.Lock()

    def __init__(self):
        self._procedure = db_procedure.db_procedure()
        self._log_info = log.MakeLog(etc.log_for_process)
        self._log_error = log.MakeLog(etc.error_for_process)
        self._log_info.start()
        self._log_error.start()
        self._task_q = task_queue.TaskQueue.instance()
        s_thread = send_thread.SendThread()
        s_thread.setDaemon(True)
        s_thread.start()

    @staticmethod
    def instance():
        if not hasattr(DatabaseManager, "_instance"):
            with DatabaseManager._instance_lock:
                if not hasattr(DatabaseManager, "_instance"):
                    DatabaseManager._instance = DatabaseManager()
        return DatabaseManager._instance

    def close(self):
         self._procedure.close()


    def db_apply_task_v2(self, apply_task_info):
          try:
             uid = apply_task_info.uid
             task_count = apply_task_info.apply_num
             if task_count < 0 or task_count > 1000:
                 resean = "task_count is invalid!  task_count < 0 or task_count > 1000"
                 self._log_info.logerror(resean)
                 return (constant.FAIL, resean)
             if uid == "":
                  resean = "uid in db_apply_task_v2 is null, invalid!"
                  self._log_info.logerror(resean)
                  return (constant.FAIL, resean)
             info_str = "uid: %d, task_count:%d" % (uid, task_count)
             #(ret_call, res) = self._procedure.call_proc_apply_task(uid, task_count)
             (ret_call, res) = self._procedure.call_proc_apply_task_v2(apply_task_info)
             if ret_call == constant.FAIL:
                resean = "there has exception in db_apply_task_v2 %s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL, resean)
             elif ret_call == constant.NOT_EXISTS:
                resean = "there has no record to apply task. %s"  % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, resean)
             else:
                resean = "%d db db_apply_task_v2 ok" % (uid)
                print resean, res
                self._log_info.loginfo(resean)
                return (constant.SUCCESS, res)
          except Exception, e:
              print e
              resean = "there has exception in db_apply_task_v2 with uid:%d, task_count:%d, error: %s"  % (uid, task_count, str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)
    
    def db_all_tasklist(self, uid, page_size, page=1, data_dic={}):
        pytools.show_value(data_dic)
        try:
             info_str = "uid: %d, db_all_tasklist page_size :%d" % (uid, page_size)
             
             (code, num, ret_dict) = self._procedure.call_all_tlist_proc(uid, page_size , page, data_dic)
             if code == constant.FAIL:
                resean = "there has exception in call_all_tlist_proc.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL, resean, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get db_all_tasklist.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, 0, resean)
             else:
                #resean = " get db_pending_tasklist ok."
                self._log_info.loginfo("get db_all_tasklist ok. " + info_str)
                return (constant.SUCCESS, num, ret_dict)
        except Exception, e:
              resean = "there has exception in db_all_tasklist with  page_size:%d, error: %s"  % (page_size, e)
              self._log_info.logerror(resean)
              return (constant.FAIL, resean, resean)

    def db_pending_tasklist(self, uid, page_size, page=1,data_dic={}):
        pytools.show_value(data_dic)
        try:
           
             (code, num, ret_dict) = self._procedure.call_pending_tlist_proc(uid, page_size , page, data_dic)
             if code == constant.FAIL:
                resean = "there has exception in call_pending_tlist_proc.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL, 0, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get db_pending_tasklist.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS,0, resean)
             else:
                
                return (constant.SUCCESS, num, ret_dict)
        except Exception, e:
              resean = "there has exception in db_pending_tasklist with  page_size:%d, error: %s"  % (page_size, str(e))
              #print resean
              self._log_info.logerror(resean)
              return (constant.FAIL,0, resean)

    def db_next_pending_task(self, uid):
        try:
             (code, ret_dict) = self._procedure.call_get_next_pending_task(uid)
             if code == constant.FAIL:
                resean = "there has exception in db_next_pending_task.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL,  resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get db_next_pending_task.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, resean)
             else:
                return (constant.SUCCESS,  ret_dict)
        except Exception, e:
              resean = "there has exception in db_next_pending_task  error: %s"  % (str(e))
              #print resean
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)

    def db_pass_tasklist(self, uid, page_size, page=1, data_dic={}):
        pytools.show_value(data_dic)
        try:
             info_str = "uid: %d db_pass_tasklist" % (uid)
           
             (code, num, ret_dict) = self._procedure.call_pass_tlist_proc(uid, page_size, page, data_dic)
             if code == constant.FAIL:
                resean = "there has exception in call_pass_tlist_proc.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL, None, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get db_pass_tasklist.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, 0, resean)
             else:
                #resean = " get db_pending_tasklist ok."
                self._log_info.loginfo("get db_pass_tasklist ok. " + info_str)
                return (constant.SUCCESS,num, ret_dict)
        except Exception, e:
              resean = "there has exception in db_pass_tasklist with uid:%d,  error: %s"  % (uid,  e)
              self._log_info.logerror(resean)
              return (constant.FAIL, resean ,resean)

    def db_failed_tasklist(self, uid, page_size, page=1, data_dic={}):
        pytools.show_value(data_dic)
        try:
             info_str = "uid: %d db_failed_tasklist" % (uid)
             
             (code, num, ret_dict) = self._procedure.call_failed_tlist_proc(uid, page_size, page, data_dic)
             if code == constant.FAIL:
                resean = "there has exception in db_failed_tasklist.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.FAIL, resean, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get db_failed_tasklist.%s" % (info_str)
                self._log_info.logerror(resean)
                return (constant.NOT_EXISTS, resean, resean)
             else:
                #resean = " get db_pending_tasklist ok."
                self._log_info.loginfo("get db_failed_tasklist ok. " + info_str)
                return (constant.SUCCESS, num, ret_dict)
        except Exception, e:
              resean = "there has exception in db_failed_tasklist with uid:%d,  error: %s"  % (uid,  e)
              self._log_info.logerror(resean)
              return (constant.FAIL, resean, resean)


    def db_cancel_audit_task(self, uid, tidlist):  #tidlist列表[]
        try:
            #loop for each tid.
            if len(tidlist) == 0:
                resean = "uid: %d, there has no tidlist to cancel_task." % (uid)
                return constant.NOT_EXISTS
            #for tid in tidlist:
            #    (code, res) = self._db_cancel_task_item(uid, tid)
            (code, res) = self._procedure.call_cancel_audit_task_proc(uid, tidlist)
            if code != constant.SUCCESS:
                return code
            return constant.SUCCESS
        except Exception, e:
              resean = "there has exception in db_cancel_audit_task with uid:%d, tid:%s, error: %s"  % (uid, tid, e)
              self._log_info.logerror(resean)
              return constant.FAIL
    
    def produce_examresult(self, tid, funshion_id, state):
        try:
            
            dict = {"tid":tid, "info":[{"funshion_id":funshion_id, "state":state}]}
            return json.dumps(dict)
        except Exception,e:
            print 'produce_examresult has except ', e
            return None


    #审核通过后通知audit_report 审核通过examresult包
    def audit_crane_examresult_task(self, tid, funshion_id):
        try:
             (code, res) = self._procedure.call_examresult_task_proc(tid, funshion_id)
             resean =  "db_audit_examresult_task tid:%s , funshion_id:%s ok" % (tid, funshion_id)
             if code == constant.FAIL:
                resean = "there has exception in db_audit_examresult_task with tid:%s, funshion_id: %s"  % (tid, funshion_id)        
                self._log_info.logerror(resean)
                return constant.FAIL
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to examresult with tid:%s, funshion_id: %s"  % (tid, funshion_id)             
                self._log_info.logerror(resean)
                return constant.NOT_EXISTS
             state = None
             res = json.loads(res)
             status = int(res['flag'])
             if status == 1:
                 state = "yes"
             else:
                 state = "no"
                 return constant.SUCCESS
             
             json_report =   self.produce_examresult(tid, funshion_id, state)
             if json_report != None:   #post the ip
                 ip = res['ip']
                 port = res['port']
                 task = task_queue.TaskSendInfo(ip, port, json_report)
                 self._task_q.add_task(task)
                 print 'add task ok with ',tid
             return constant.SUCCESS
        except Exception, e:
              print 'audit_crane_examresult_task error', e
              resean = "there has exception in audit_crane_examresult_task with tid:%s, funshion_id:%s, error: %s"  % (tid, funshion_id, str(e))
              self._log_info.logerror(resean)
              return constant.FAIL


    def audit_cloud_result_task(self, tid):
        try:
            #get the task_id from tid by db opt.
            (code, task_id) = self._procedure.call_cloud_get_taskid_bytid(tid)
            if code != constant.SUCCESS:
                resean = "there has error with call_cloud_get_taskid_bytid from tid : %s"  % (tid)
                print resean
                return constant.FAIL
            
            cloud_task = task_queue.CloudTask(task_id)
            self._task_q.add_task(cloud_task)
            print 'cloud process task_id: ', task_id
            return constant.SUCCESS
        except Exception,e:
            return constant.FAIL


    def db_audit_video_task(self, uid, tid,  funshion_id, result, modifyInfo):  #result：1-通过， 0--不通过
        try:
            print 'cloud audit_video_task: ', uid, tid, funshion_id, result
            (code, res_tid) = self._procedure.call_audit_video_task_proc(uid, tid, funshion_id, result, modifyInfo)
            print 'db_audit_video_task yes ', code, res_tid
            #if code != constant.SUCCESS:
            #    return code

            #notify the service to examresult.
            #code =  self.audit_crane_examresult_task(tid, funshion_id)

            if result == 1:
                code =  self.audit_cloud_result_task(tid)   # for cloud_Centaurus service.
                if code == constant.FAIL:
                    resean = "in db_audit_video_task::db_audit_examresult_task error with tid:%s, funshion_id: %s"  % (tid, funshion_id)
                    self._log_info.logerror(resean)
                    return constant.FAIL
            return constant.SUCCESS
        except Exception, e:
              print 'db_audit_video_task error, ', e
              resean = "there has exception in db_cancel_audit_task with uid:%d, tid:%s, error: %s"  % (uid, tid, e)
              self._log_info.logerror(resean)
              return constant.FAIL

    def db_get_audit_task_details(self, tid): 
        try:
            #loop for each tid.
            (code, ret_res) = self._procedure.call_get_task_details_proc(tid)
            if code != constant.SUCCESS:
                return (code, ret_res)
            return (constant.SUCCESS, ret_res)
        except Exception, e:
              resean = "there has exception in db_get_audit_task_details with  tid:%s, error: %s"  % (tid, e)
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)
   
   
    def db_get_video_base(self, tid): 
        try:
            #loop for each tid.
            (code, ret_res) = self._procedure.call_get_video_base_proc(tid)
            if code != constant.SUCCESS:
                return (code, ret_res)
            return (constant.SUCCESS, ret_res)
        except Exception, e:
              resean = "there has exception in db_get_video_base with  tid:%s, error: %s"  % (tid, e)
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)


    def db_get_forwards_userspace(self, uid, page_size, page): 
        try:
            #get number.
            if (page_size== -1):  #get the db_get_forwards_userspace number.
                 (code, count) = self._procedure.call_get_total_number_proc(uid, 'forward_space')
                 if code != constant.SUCCESS:
                     resean = " db_get_forwards_userspace error.%s" % (info_str)
                     self._log_info.logerror(resean)
                     return (constant.FAIL, resean)
                
                 return (constant.SUCCESS, count)
            #loop for each tid.
            (code, ret_res) = self._procedure.call_get_forwards_userspace(uid, page_size, page)
            if code != constant.SUCCESS:
                return (code, ret_res)
            return (constant.SUCCESS, ret_res)
        except Exception, e:
              print e
              resean = "there has exception in db_get_forwards_userspace with uid:%d, error: %s"  % (uid, str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)

    def db_get_forwards_userspace_v2(self, uid, page_size, page, origin="forwards"): 
        try:
            result = self._procedure.call_get_forwards_userspace_v2(uid, page_size, page, origin)
            if result[0] == constant.SUCCESS:
                return (result[0],result[1],result[2])
            return (constant.FAIL,None)
        except Exception, e:
              print e
              resean = "there has exception in db_get_forwards_userspace with uid:%d, error: %s"  % (uid, str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean)

    def db_get_video_msinfo(self,tid):
        return self._procedure.call_get_video_msinfo(tid)

    def db_get_audit_statics_info(self, begin_time, end_time, page_size, page): 
        with DatabaseManager._instance_lock:
            try:
                #get number.

                #loop for each tid.
                (code, user_num,ret_list, total_list) = self._procedure.call_get_audit_statics_info_v3(begin_time, end_time, page_size, page)
                if code != constant.SUCCESS:
                    return (code, None, None, None)
                return (constant.SUCCESS,user_num, ret_list, total_list)
            except Exception, e:
                  print 'db_get_audit_statics_info error', e
                  resean = "there has exception in db_get_audit_statics_info with time:%s, error: %s"  % (time, str(e))
                  self._log_info.logerror(resean)
                  return (constant.FAIL, resean, resean, resean)
   

    def db_get_dat_macros_statics(self, begin_time, end_time, page_size, page): 
        try:
            (code, num, result) = self._procedure.call_dat_statics_info(begin_time, end_time, page_size, page)
            if code == constant.SUCCESS:
                return (code, num, result)
            return (constant.FAIL, 0, None)
        except Exception, e:
              print e
              reason = "there has exception in db_get_dat_macros_statics with uid:%d, error: %s"  % (uid, str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, 0, reason)


    def db_search_mp4info_from_dat(self, key_search, key_type, page_size, page): 
        try:
            result = self._procedure.call_dat_search_funshionlist(key_search, key_type, page_size, page)
            if result[0] == constant.SUCCESS:
                return (result[0],result[1],result[2])
            return (constant.FAIL,None)
        except Exception, e:
              print e
              resean = "there has exception in db_search_mp4info_from_dat with uid:%d, error: %s"  % (uid, str(e))
              self._log_info.logerror(resean)
              return (constant.FAIL, resean, resean)



