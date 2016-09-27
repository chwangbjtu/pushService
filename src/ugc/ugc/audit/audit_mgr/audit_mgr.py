#!/bin/env python
# -*- coding: utf-8    -*- 
#interface class.
import json
import threading
import pytools

import db_mgr
import constant
import http_client
import etc
from audit_modify_info import AuditModifyInfo

class AuditMgr(threading.Thread):
    _instance_lock = threading.Lock()

    def __init__(self):
        self._audit_dbmgr = db_mgr.DatabaseManager.instance()

    @staticmethod
    def instance():
        if not hasattr(AuditMgr, "_instance"):
            with AuditMgr._instance_lock:
                if not hasattr(AuditMgr, "_instance"):
                    AuditMgr._instance = AuditMgr()
        return AuditMgr._instance

    def close(self):
        self._audit_dbmgr.close()


     #申请任务
    def apply_task(self, apply_task_info):
       try:
             (code, ret_call) = self._audit_dbmgr.db_apply_task_v2(apply_task_info)
             if code == constant.FAIL:
                resean = "there has exception in DatabaseManager with apply_task_v2."
                print resean
                return (constant.FAIL, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to apply_task_v2."
                print resean
                return (constant.NOT_EXISTS, resean)
             else:
                resean = "apply_task_v2 ok."
                #print resean
                return (constant.SUCCESS, ret_call)
       except Exception, e:
              resean = "there has exception in apply_task_v2 with %s" % e
              print resean
              return (constant.FAIL, resean)
    #筛选任务
    def filter_task(self, apply_task_info):
       try:
             (code, ret_call) = self._audit_dbmgr.db_apply_task_v2(apply_task_info)
             if code == constant.FAIL:
                resean = "there has exception in DatabaseManager with apply_task_v2."
                print resean
                return (constant.FAIL, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to apply_task_v2."
                print resean
                return (constant.NOT_EXISTS, resean)
             else:
                resean = "apply_task_v2 ok."
                #print resean
                return (constant.SUCCESS, ret_call)
       except Exception, e:
              resean = "there has exception in apply_task_v2 with %s" % e
              print resean
              return (constant.FAIL, resean)

    #获取所有任务列表
    #当uid = None, 获取所有任务列表
    def get_all_tasklist(self, uid, page_size, page, data_dic={}):
         pytools.show_value(data_dic)
         try:
             (code, num, ret_dict) = self._audit_dbmgr.db_all_tasklist(uid,  page_size, page, data_dic)
             #print code, ret_dict
             if code == constant.FAIL:
                resean = "there has exception in get_all_tasklist."
                return (constant.FAIL, 0, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_all_tasklist."
                return (constant.NOT_EXISTS, 0, resean)
             else:
                resean = " get_all_tasklist ok."
                print resean
                return (constant.SUCCESS, num,ret_dict)
         except Exception, e:
              resean = "there has exception in  get_all_tasklist with %s" % e
              return (constant.FAIL, 0, resean)

    #获取待审核任务列表
    #当uid = None, 获取所有任务列表
    def get_pending_tasklist(self, uid, page_size, page, data_dic={}):
         pytools.show_value(data_dic)
         try:
             (code, num, ret_dict) = self._audit_dbmgr.db_pending_tasklist(uid,  page_size, page, data_dic)
             #print code, ret_dict
             if code == constant.FAIL:
                resean = "there has exception in call_pending_tlist_proc."
                return (constant.FAIL, 0,resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_pending_tasklist."
                return (constant.NOT_EXISTS, 0,resean)
             else:
                resean = " get_pending_tasklist ok."
                print resean
                return (constant.SUCCESS, num,ret_dict)
         except Exception, e:
              resean = "there has exception in  db_pending_tasklist with %s" % e
              return (constant.FAIL, 0,resean)

    def get_next_task(self, uid):
         try:
             (code, audit_info) = self._audit_dbmgr.db_next_pending_task(uid)
             #print code, ret_dict
             if code == constant.FAIL:
                resean = "there has exception in call_pending_tlist_proc."
                return (constant.FAIL, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_pending_tasklist."
                return (constant.NOT_EXISTS, resean)
             else:
                resean = " get_pending_tasklist ok."
                print resean
                return (constant.SUCCESS, audit_info)
         except Exception, e:
              resean = "there has exception in  db_pending_tasklist with %s" % e
              return (constant.FAIL, resean)


    #获取已审核任务列表
    def get_passed_tasklist(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic)
        try:
             
             (code, num, ret_dict) = self._audit_dbmgr.db_pass_tasklist(uid, page_size, page, data_dic)
             #print code, ret_dict
             if code == constant.FAIL:
                resean = "there has exception in db_pass_tasklist."
                return (constant.FAIL, 0 , resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_passed_tasklist."
                return (constant.NOT_EXISTS, 0, resean)
             else:
                resean = " get_passed_tasklist ok."
                print resean
                return (constant.SUCCESS, num, ret_dict)
        except Exception, e:
              resean = "there has exception in  get_passed_tasklist with %s" % e
              return (constant.FAIL, 0, resean)


     #获取审核失败任务列表
    def get_failure_tasklist(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic)
        try:
         
             (code, num, ret_dict) = self._audit_dbmgr.db_failed_tasklist(uid, page_size, page, data_dic)
             print code, ret_dict
             if code == constant.FAIL:
                resean = "there has exception in get_failure_tasklist."
                return (constant.FAIL, 0, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_failure_tasklist."
                return (constant.NOT_EXISTS, 0, resean)
             else:
                resean = " get_failure_tasklist ok."
                print resean
                return (constant.SUCCESS, num,ret_dict)
        except Exception, e:
              resean = "there has exception in  get_failure_tasklist with %s" % e
              return (constant.FAIL, 0, resean)

    #退订审核任务
    #tid_list： 列表 eg： ['1111X','2222y','33333zzz'] 
    def cancel_task(self, uid, tid_list):
        try:
             if uid == None:
                 resean = "uid == None"
                 return (constant.FAIL, resean)
             code = self._audit_dbmgr.db_cancel_audit_task(uid, tid_list)
             print code
             if code == constant.FAIL:
                resean = "there has exception in cancel_task."
                return (constant.FAIL, resean)
             elif code == constant.NOT_EXISTS:
                resean = "there has no record to cancel_task."
                return (constant.NOT_EXISTS, resean)
             else:
                resean = "uid %d cancel_task ok." % uid
                print resean
                return (constant.SUCCESS, resean)
        except Exception, e:
              resean = "there has exception in  cancel_task with %s" % e
              return (constant.FAIL, resean)
    
    def _compose_audit_report(self, uid, tid, funshion_id, result, modifyInfo = None):
        report = {}
        report['uid'] = uid
        report['tid'] = tid
        report['fid'] = funshion_id
        if result == 1:
            report['pass']      = True
        else:
            report['pass'] = False
            
        if modifyInfo:
            report['title']     = modifyInfo.title
            report['channel']   = modifyInfo.channel
            report['tags']      = modifyInfo.tags
            report['description'] = modifyInfo.description
            report['logo']      = modifyInfo.logo
            report['ttype']     = modifyInfo.ttype
        return report
        
    #审核视频 #result: 1---通过, 0--未通过
  # def audit_video(self, uid, tid, result, info_changed = ""):
    def audit_video(self, uid, tid, funshion_id, result, modifyInfo=None):    #input the AuditModifyInfo inst.
        try:
            if uid == None:
                 resean = "uid == None"
                 return (constant.FAIL, resean)
            report = self._compose_audit_report(uid, tid, funshion_id, result, modifyInfo)
            
            ok = http_client.post_audit_task(etc.MAZE_SERVICE_IP, etc.MAZE_SERVICE_PORT, json.dumps(report))
            #code = self._audit_dbmgr.db_audit_video_task(uid, tid, funshion_id, result, modifyInfo)
            if not ok: #code == constant.FAIL:
                resean = "can not submit audti to maze ......"
                return (constant.FAIL, resean)
            # elif code == constant.NOT_EXISTS:
                # resean = "there has no record to audit_video."
                # return (constant.NOT_EXISTS, resean)
            # elif code == constant.FORBIDDEN:
                # resean = "审核视频任务 %s 无效！" % (tid)
                # print resean
                # return (constant.FORBIDDEN, resean)
            else:
                resean = "uid %d audit_video %s ok." % (uid, tid)
                #print resean
                return (constant.SUCCESS, resean)
       
        except Exception, e:
            print e
            resean = "there has exception in  audit_video with %s" % e
            return (constant.FAIL, resean)

    #由tid获取详细审核信息
    def get_audit_task_details(self, tid):
        try:
            (code, res) = self._audit_dbmgr.db_get_audit_task_details(tid)
            if code == constant.FAIL:
                resean = "there has exception in get_audit_task_details."
                return (constant.FAIL, resean)
            elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_audit_task_details."
                return (constant.NOT_EXISTS, resean)
            else:
                #resean = "uid %d get_audit_task_details %s ok." % (uid, tid)
                #print resean
                return (constant.SUCCESS, res)
        except Exception, e:
            print e
            resean = "there has exception in  get_audit_task_details with %s" % e
            return (constant.FAIL, resean)

    #获取基础数据，由tid提取
    def get_video_base(self, tid):
        try:
            (code, res) = self._audit_dbmgr.db_get_video_base(tid)
            if code == constant.FAIL:
                resean = "there has exception in db_get_video_base."
                return (constant.FAIL, resean)
            elif code == constant.NOT_EXISTS:
                resean = "there has no record to db_get_video_base."
                return (constant.NOT_EXISTS, resean)
            else:
                #resean = "uid %d get_audit_task_details %s ok." % (uid, tid)
                #print resean
                return (constant.SUCCESS, res)
        except Exception, e:
            print e
            resean = "there has exception in  db_get_video_base with %s" % e
            return (constant.FAIL, resean)


     #获取转帖用户任务列表，由uid提取
    def get_forwards_userspace(self, uid, page_size, page):
        try:
            (code, res) = self._audit_dbmgr.db_get_forwards_userspace(uid, page_size, page)
            if code == constant.FAIL:
                resean = "there has exception in get_forwards_userspace."
                return (constant.FAIL, resean)
            elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_forwards_userspace."
                return (constant.NOT_EXISTS, resean)
            else:
                #resean = "uid %d get_audit_task_details %s ok." % (uid, tid)
                #print resean
                return (constant.SUCCESS, res)
        except Exception, e:
            print e
            resean = "there has exception in  get_forwards_userspace with %s" % e
            return (constant.FAIL, resean)

    def get_forwards_userspace_v2(self, uid, page_size, page, origin="forwards"):
        return self._audit_dbmgr.db_get_forwards_userspace_v2(uid, page_size, page, origin)

    def get_video_msurl(self,tid):
        result = self._audit_dbmgr.db_get_video_msinfo(tid)
        if result[0] == constant.SUCCESS and result[1]:
            funshion_id,dat_id,ms_ip = (result[1][0],result[1][1],result[1][2])
            url = "http://%s:80/play/%s/%s.mp4" % (ms_ip, dat_id, funshion_id)
            return url
        return None

    #获取审核统计信息，由time时间按照天来获取
    def get_audit_statics_info(self,  begin_time, end_time, page_size, page):
        try:
            (code, user_num,ret_list, total_list) = self._audit_dbmgr.db_get_audit_statics_info(begin_time, end_time, page_size, page)
            if code == constant.FAIL:
                resean = "there has exception in get_audit_statics_info."
                return (constant.FAIL, 0, resean, resean)
            elif code == constant.NOT_EXISTS:
                resean = "there has no record to get_audit_statics_info."
                return (constant.NOT_EXISTS, 0,resean,resean)
           
            return (constant.SUCCESS, user_num,ret_list, total_list)
        except Exception, e:
            print e
            resean = "there has exception in  get_audit_statics_info with %s" % e
            return (constant.FAIL, 0, resean,resean)

    def get_dat_macros_statics_list(self, begin_time, end_time,  page_size, page):
        return self._audit_dbmgr.db_get_dat_macros_statics(begin_time, end_time, page_size, page)


    #key_search : key_type='dat', key_search 为dat_id,   key_type='funshion', key_search 为funshion_id
    def search_mp4_info_from_dat(self, key_search, key_type,  page_size, page):
        return self._audit_dbmgr.db_search_mp4info_from_dat(key_search, key_type, page_size, page)

