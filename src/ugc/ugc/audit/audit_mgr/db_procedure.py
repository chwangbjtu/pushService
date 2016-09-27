#!/bin/env python
# -*- coding: utf-8    -*- 
import etc
import log
import json
import constant
import MySQLdb
import db_connect
import audit_task

from  datetime  import  *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from  audit_modify_info import AuditModifyInfo
from  audit_modify_info import ApplyTaskInfo
from  audit_statics_info import AuditStaticsList
import pytools
import sql_helper

def get_search_str(data_dic, uid=-1):
    pytools.show_value(data_dic)
    search_str = ""
    search_item = data_dic.get('search','').strip()
    #if uid == -1:
    #    if search_item: search_str = 'where %s' % search_item
   # else:
    if search_item: 
        search_str = 'and ugc_video.%s' % search_item
    return search_str

def get_order_str(data_dic={}):
    pytools.show_value(data_dic)
    order_str=""
    order_item = data_dic.get('order','').strip()
    pytools.show_value(order_item,'order_item')
    if order_item: 
        order_str = ', %s' % order_item
    else:
        order_str = ', time desc'

    return order_str

def get_ret_str():
    return 'tid, uid, title, tags, channel, step, status, funshion_id, time, duration, username, vid, priority'
    #return 'tid, uid, title, tags, channel, step, status, funshion_id, time, duration, username'

class db_procedure:
    def __init__(self):
        self.__proc_info = log.MakeLog(etc.log_for_procedure)
        self.__proc_error = log.MakeLog(etc.error_for_procedure)
        self.__proc_info.start()
        self.__proc_error.start()

    def close(self):
        pass

    def call_proc_with_db(self,  proc_name, tuple_list):
        try:
            dbconn = db_connect.DBConnect()
            ret = dbconn.call_proc_db(proc_name, tuple_list)
            if  ret == None:
                info = "there has error in call_proc_db  with %s" % (proc_name)
                print info
                self.__proc_info.logerror(info)
                dbconn.close()
                return (constant.NOT_EXISTS, None)
            else:
                dbconn.close()
                return (constant.SUCCESS, ret)
        except Exception, e:
            errinfo = "there has exception in operate_with_db with %s, %s" % (connstr, str(e))
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, None)

    def fetch_info_with_db(self,  connstr):
        try:
            dbconn = db_connect.DBConnect()
            db_records = dbconn.db_fetchall(connstr)
            if not db_records:
                info = "there has no record in  with %s" % (connstr)
                self.__proc_info.logerror(info)
                dbconn.close()
                return (constant.NOT_EXISTS, None)
            else:
                dbconn.close()
                return (constant.SUCCESS, db_records)
        except Exception, e:
            errinfo = "there has exception in fetch_info_with_db with %s, %s" % (connstr, str(e))
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, None)

    def produce_condition(self, apply_task_info):
        try:
            site = apply_task_info.site
            channel = apply_task_info.channel
            title = apply_task_info.title
            begin_time = apply_task_info.begin_time
            end_time = apply_task_info.end_time
            connstr = None
            condition = None
            if site == "" and channel == "" and title == "" and begin_time == "" and end_time == "":
                condition = "where step='audit' and status=0"
            elif site != "" and channel == "" and title == "" and begin_time == "" and end_time == "":
                condition = "where step='audit' and status=0 and site='%s'" % (site)
            elif site != "" and channel != "" and title == "" and begin_time == "" and end_time == "":
                condition = "where step='audit' and status=0 and site='%s' and channel='%s'" % (site, channel)
            elif site != "" and channel != "" and title != "" and begin_time == "" and end_time == "":
                temp_title = "'%"+"%s" % (title)+"%'"
                condition = "where step='audit' and status=0 and site='%s' and channel='%s' and  title LIKE %s" % (site, channel, temp_title)
            elif site == "" and channel != "" and title == "" and begin_time == "" and end_time == "":
                condition = "where step='audit' and status=0 and  channel='%s'" % (channel)
            elif site == "" and channel == "" and title != "" and begin_time == "" and end_time == "":
                temp_title = "'%"+"%s" % (title)+"%'"
                condition = "where step='audit' and status=0 and  title LIKE %s" % (temp_title)
            elif site != "" and channel == "" and title != "" and begin_time == "" and end_time == "":
                temp_title = "'%"+"%s" % (title)+"%'"
                condition = "where step='audit' and status=0 and site='%s' and  title LIKE %s" % (site, temp_title)
            elif site == "" and channel != "" and title != "" and begin_time == "" and end_time == "":
                temp_title = "'%"+"%s" % (title)+"%'"
                condition = "where step='audit' and status=0 and channel='%s' and  title LIKE %s" % (channel, temp_title)
            elif site == "" and channel == "" and title == "" and begin_time != "" and end_time != "":
                condition = "where step='audit' and status=0 and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (begin_time, end_time)
            elif site != "" and channel == "" and title == "" and begin_time != "" and end_time != "":
                condition = "where step='audit' and status=0 and site='%s' and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (site, begin_time, end_time)
            elif site != "" and channel != "" and title == "" and begin_time != "" and end_time != "":
                condition = "where step='audit' and status=0 and site='%s'  and channel='%s' and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (site, channel, begin_time, end_time)
            elif site == "" and channel != "" and title == "" and begin_time != "" and end_time != "":
                condition = "where step='audit' and status=0 and channel='%s' and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (channel, begin_time, end_time)
            elif site == "" and channel == "" and title != "" and begin_time != "" and end_time != "":
                temp_title = "'%"+"%s" % (title)+"%'"
                condition = "where step='audit' and status=0 and title LIKE %s and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (temp_title, begin_time, end_time)
            elif site == "" and channel == "" and title == "" and begin_time != "" and end_time == "":
                end_time = date.today()
                condition = "where step='audit' and status=0 and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (begin_time, end_time)
            elif site == "" and channel == "" and title == "" and begin_time == "" and end_time != "":
                begin_time = "2000-01-01"
                condition = "where step='audit' and status=0 and  ctime BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (begin_time, end_time)
            else:
                condition = "where step='audit' and status=0"
            
            condition = condition + " and audit_free = 0"
            return condition
        except Exception, e:
            errinfo = "there has exception in produce_condition with  %s" % ( str(e)) 
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  None


    #申请任务,带过滤功能
    def call_proc_apply_task_v2(self, apply_task_info):
        try:
            uid = apply_task_info.uid
            apply_num = apply_task_info.apply_num
            f_username = apply_task_info.f_username    #任务的创建者（或者转帖，上传）
            print 'value:',uid, 'num: ', apply_num,' name: ',f_username
            if apply_num == 0 or uid == -1:
                 errinfo = "apply_task error is invalid, %d, %d" % (uid, apply_num)
                 print errinfo
                 self.__proc_error.logerror(errinfo)
                 return  (constant.FAIL, errinfo)

            condition = self.produce_condition(apply_task_info)
            if condition == None:
                errinfo = "produce_condition error."
                return  (constant.FAIL, errinfo)

            if f_username == '':
                f_username = "None"
            #connstr = "call proc_apply_task_v2(%d, %d, \"%s\",'%s')" % (uid, apply_num, condition, f_username)
            proc_name = "proc_apply_task_v2"
            #print connstr
            (code, db_records) = self.call_proc_with_db(proc_name, (int(uid), int(apply_num), condition, f_username))
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.FAIL, 0)

            #ret_count = 0
            ret_count = db_records[0]
            if ret_count >=  apply_num:  #get the count.
                ret_count = apply_num
            
            print 'apply_task_v2 ok',  ret_count
            return (constant.SUCCESS, ret_count)
        except Exception, e:
            errinfo = "there has exception in call_proc_apply_task with %d, %s" % (uid, str(e))
            print errinfo
            self.__proc_error.logerror(errinfo)
            return  (constant.FAIL, None)

    def create_duration(self, duration):
        try:
            import time
            createValue = duration
            createValue = float(createValue)
            createValue /= 1000
            return str(time.strftime('%H:%M:%S', time.gmtime(createValue)))
        except Exception, e:
            return None

    def produce_json(self, data):
        try:
            ret_list = []
            check_map = {}
            for rec in data:
                ret_dict = {}
                tid = rec[0]
                if check_map.has_key(tid):
                    continue
                check_map[tid] = tid
                ret_dict['tid'] = rec[0]
                ret_dict['uid'] = rec[1]
                ret_dict['title'] = rec[2]
                ret_dict['tags'] = rec[3]
                ret_dict['channel'] = rec[4]
                ret_dict['step'] = rec[5]
                ret_dict['funshion_id'] = rec[7]
                ret_dict['time'] = str(rec[8])
                duration = self.create_duration(rec[9])
                if duration != None:
                    ret_dict['duration'] = str(duration)
                username = rec[10]
                if username != None:
                    ret_dict['username'] = username
                try:
                    ret_dict['vid'] = str(rec[11])
                    ret_dict['priority'] = str(rec[12])
                except Exception,e:
                    pytools.show_error(e)
                ret_list.append(json.dumps(ret_dict))
            return ret_list
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in produce_json.%s" % e 
            self.__proc_error.logerror(errinfo)
            return None

     #获取所有任务列表
    def call_all_tlist_proc(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic)
        search_str = get_search_str(data_dic, uid)
        order_str = get_order_str(data_dic)
        ret_str = get_ret_str()
        ret_list = []
        try:
            cur_page = page
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_page_get_all_task",(cur_page, page_size, uid, search_str))
            if not cursor:
                return (constant.FAIL, 0, None)
            alltask_num = cursor.fetchone()
            alltask_num = alltask_num[0]
            cursor.nextset()
            db_records = cursor.fetchall()
            if db_records == None:
                print 'None db_records'
                return (constant.SUCCESS, 0, ret_list)
            
            ret_list = self.produce_json(db_records)
            if ret_list == None:
                print 'produce_json error.'
                errinfo = "call_all_tlist_proc in produce_json has error with: %s" % connstr 
                self.__proc_error.logerror(errinfo)

            dbconn.close()
            pytools.show_value(ret_list,'ret_list')

            return (constant.SUCCESS, alltask_num , ret_list)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_all_tlist_proc.%s" % str(e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, 0, None)


     #获取待审核任务列表
    def call_pending_tlist_proc(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic)
        search_str = get_search_str(data_dic, uid)
        order_str = get_order_str(data_dic)
        ret_str = get_ret_str()

        ret_list = []
        try:
            cur_page = page
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_page_get_pending_tasks",(cur_page, page_size, uid, search_str))
            if not cursor:
                return (constant.FAIL, None, None)
            pending_num = cursor.fetchone()
            pending_num = pending_num[0]
            cursor.nextset()
            db_records = cursor.fetchall()
            if db_records == None:
                print 'None db_records'
                return (constant.SUCCESS,ret_list, ret_list)
            #print 'pending task.',db_records
            ret_list = self.produce_json(db_records)
            if ret_list == None:
                print 'produce_json error.'
                errinfo = "call_pending_tlist_proc in produce_json has error with: %s" % connstr 
                self.__proc_error.logerror(errinfo)
            dbconn.close()
            pytools.show_value(ret_list,'ret_list')
            return (constant.SUCCESS, pending_num, ret_list)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in get_pending_tasklist.%s" % str(e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, errinfo, errinfo)


    def input_info_audit_video_info(self, rec_map):
        try:
            print type(rec_map),rec_map
            import ugc.audit.audit_video_info
            audit_info =  ugc.audit.audit_video_info.AuditVideoInfo()
            funshion_info = ugc.audit.audit_video_info.FunshionInfo()
            audit_info.tid = rec_map['tid']
            audit_info.uid  =  rec_map['uid']
            audit_info.user = rec_map['username']
            audit_info.title =   rec_map['title']
            audit_info.origin = "spider"
            audit_info.tags = rec_map['tags']
            audit_info.channel = rec_map['channel']
            audit_info.description = rec_map['description']
            audit_info.ttype = 0
            audit_info.seconds = rec_map['duration']
            audit_info.step = "audit"
            audit_info.status = 0
            audit_info.video_id = "0"
            audit_info.priority = rec_map['priority']
            funshion_info.funshion_id = rec_map['funshion_id']
            funshion_info.rate = rec_map['rate']
            funshion_info.file_size = rec_map['filesize'] 
            funshion_info.filename = rec_map['filename']
            funshion_info.video_url = rec_map['video_url']
            funshion_info.small_image = rec_map['small_image']
            funshion_info.large_image = rec_map['large_image']
            funshion_info.logo = rec_map['logo']
            funshion_info.duration = rec_map['duration']
            audit_info.funshion_list[funshion_info.rate] = funshion_info
            return audit_info
        except Exception,e:
            print 'input_info_audit_video_info error', e
            return None


    #自动获取下一个待审核的任务
    def call_get_next_pending_task(self, uid):
        try:
           
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_get_next_task",(uid,))
            if not cursor:
                return (constant.FAIL, None)
            
            db_records = cursor.fetchall()
            if len(db_records) == 0:
                print 'no task record.'
                return (constant.SUCCESS, None)
            rec_dict = self.create_details_info(db_records)
            print rec_dict
            audit_info =  self.input_info_audit_video_info(rec_dict)
            if audit_info == None:
                print 'input_info_audit_video_info error.'
                return (constant.FAIL, None)
            #ret_res = json.dumps(rec_dict)
            #print 'task_details info: ', ret_res
            #rec_list.append(ret_res)
            dbconn.close()
            return (constant.SUCCESS, audit_info)
        except Exception,e:
            print 'call_get_next_pending_task', e
            return (constant.FAIL, None)


     #获取已审核任务列表
    def call_pass_tlist_proc(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic)
        search_str = get_search_str(data_dic, uid)
        order_str = get_order_str(data_dic)
        ret_str = get_ret_str()

        ret_list = []
        try:
            cur_page = page
            
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_page_get_passed_task",(cur_page, page_size, uid, search_str))
            if not cursor:
                return (constant.FAIL, 0, None)
            passed_num = cursor.fetchone()
            passed_num = passed_num[0]
            cursor.nextset()
            db_records = cursor.fetchall()
            if db_records == None:
                print 'None db_records'
                return (constant.SUCCESS, ret_list, ret_list)
            print 'passed task.',search_str,db_records
            ret_list = self.produce_json(db_records)
            if ret_list == None:
                print 'produce_json error.'
                errinfo = "call_pass_tlist_proc in produce_json has error with: %s" % connstr 
                self.__proc_error.logerror(errinfo)

            dbconn.close()
            pytools.show_value(ret_list,'ret_list')
            return (constant.SUCCESS, passed_num, ret_list)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_pass_tlist_proc.%s" % str(e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None, None)


     #获取审核失败任务列表
    def call_failed_tlist_proc(self, uid, page_size, page, data_dic={}):
        pytools.show_value(data_dic) 
        search_str = get_search_str(data_dic, uid)
        order_str = get_order_str(data_dic)
        ret_str = get_ret_str()

        ret_list = []
        try:
            cur_page = page
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_page_get_failed_task",(cur_page, page_size, uid, search_str))
            if not cursor:
                return (constant.FAIL, None, None)
            failed_num = cursor.fetchone()
            failed_num = failed_num[0]
            cursor.nextset()
            db_records = cursor.fetchall()
            if db_records == None:
                print 'None db_records'
                return (constant.SUCCESS, ret_list, ret_list)
            #print 'failed task.',search_str,db_records
           
            ret_list = self.produce_json(db_records)
            if ret_list == None:
                print 'produce_json error.'
                errinfo = "call_failed_tlist_proc in produce_json has error with: %s" % connstr 
                self.__proc_error.logerror(errinfo)

            dbconn.close()
            pytools.show_value(ret_list,'ret_list')
            return (constant.SUCCESS, failed_num, ret_list)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_failed_tlist_proc.uid: %d, %s" % (uid, str(e)) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, errinfo, errinfo)
         

    #退订审核任务
    #def call_cancel_audit_task_proc(self, uid, tid):
    def call_cancel_audit_task_proc(self, uid, tid_list):
        try:
            flag = None
            ret_tid = None
            
            proc_name = "proc_cancel_audit_task_v2"
            ts_list = sql_helper.sql_build_value(tid_list)
            (code, db_records) = self.call_proc_with_db(proc_name, (int(uid), ts_list))
            
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.NOT_EXISTS, 0)

            #for rec in db_records:
            flag = db_records[0]
            ret_tid = db_records[1]
            return (constant.SUCCESS, ret_tid)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_cancel_audit_task_proc.tid: %s, %s" % (tid, str(e)) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)


     #审核视频图片任务
    def call_audit_video_task_proc(self, uid, tid, funshion_id, result, modifyInfo):
        try:
            if sql_helper.is_bad_sql_string(tid):
                return (constant.FAIL,"invalid args")
            ret_tid = None
            base_info_sql = ""
            audit_info_sql = ""
            if modifyInfo != None:
                #funshion_id = modifyInfo.funshion_id
                title =   modifyInfo.title
                channel = modifyInfo.channel
                tags = modifyInfo.tags
                logo = modifyInfo.logo
                description =  modifyInfo.description
                if sql_helper.exist_bad_sql_string(title,channel,tags,logo):
                    return (constant.FAIL,"invalid args")
                base_info_list = (("title",title),("channel",channel),("tags",tags), ("description",description))
                base_info_sql = sql_helper.sql_build_set_value(base_info_list)
                audit_info_list = (("logo",logo),)
                audit_info_sql = sql_helper.sql_build_set_value(audit_info_list)
            
            proc_name = "proc_audit_video_task_v2"
            (code, db_records) = self.call_proc_with_db(proc_name, (uid, tid, funshion_id, result,base_info_sql,audit_info_sql))
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.NOT_EXISTS, 0)

            #for rec in db_records:
            flag = db_records[0]
            ret_tid = db_records[1]
            if flag == "0":
                print 'forbidden.'
                return (constant.FORBIDDEN, ret_tid)
            print 'op_flag: ', flag, ', tid:',ret_tid
            return (constant.SUCCESS,ret_tid)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_audit_video_task_proc.tid: %s, %s" % (tid, e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)


    def create_details_info(self, db_records):
        try:
             rec_dict = {}
             for rec in db_records:
                rec_dict['tid'] = rec[0]
                rec_dict['uid'] = rec[1]
                rec_dict['title'] = rec[2]
                rec_dict['tags'] = rec[3]
                rec_dict['channel'] = rec[4]
                rec_dict['funshion_id'] = rec[5]
                rec_dict['filename'] = rec[6]
                rec_dict['filesize'] = rec[7]
                rec_dict['video_url'] = rec[8]
                rec_dict['small_image'] = rec[9]
                rec_dict['large_image'] = rec[10]
                rec_dict['logo'] = rec[11]
                rec_dict['rate'] = rec[12]
                rec_dict['duration'] = rec[13]
                rec_dict['description'] = rec[20]
                rec_dict['username'] = rec[18]
                rec_dict['priority'] = rec[16]
                
             return rec_dict
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in create_details_info %s" % (str(e)) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)


    def call_get_task_details_proc(self, tid):
        try:
            rec_list = []
            rec_dict = {}
            
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_get_details_info",(tid, ))
            if not cursor:
                return (constant.FAIL, None)
            
            db_records = cursor.fetchall()
         
            rec_dict = self.create_details_info(db_records)
            ret_res = json.dumps(rec_dict)
            print 'task_details info: ', ret_res
            rec_list.append(ret_res)
            return (constant.SUCCESS, rec_list)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in v_get_audit_detail_task.tid: %s, %s" % (tid, e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)

    #获取基础数据
    def call_get_video_base_proc(self, tid):
        try:
            rec_dict = {}
            connstr = "select * from v_video_base where tid='%s' limit 1" % (tid)
            print connstr
            
           # cursor = self.__conn.cursor()
            (code, db_records) = self.fetch_info_with_db(connstr)
           # cursor.close()
            #self.__db_conn.close_cursor()
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.SUCCESS, rec_dict)

            for rec in db_records:
                rec_dict['uid'] = rec[0]
                rec_dict['username'] = rec[1]
                rec_dict['tid'] = rec[2]
                rec_dict['site'] = rec[3]
                rec_dict['title'] = rec[4]
                rec_dict['tags'] = rec[5]
                rec_dict['origin'] = rec[6]
                rec_dict['channel'] = rec[7]
                rec_dict['description'] = rec[8]
                rec_dict['priority'] = rec[9]
                rec_dict['step'] = rec[10]
                rec_dict['status'] = rec[11]
                rec_dict['video_id'] = rec[12]
                rec_dict['seconds'] = rec[13]
                rec_dict['ttype'] = rec[14]
            ret_res = json.dumps(rec_dict)
            return (constant.SUCCESS, ret_res)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_get_video_base_proc.tid: %s, %s" % (tid, str(e)) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)

    def call_examresult_task_proc(self, tid, funshion_id):
        try:
            rec_dict = {}
            connstr = "select * from v_get_verify_examresult where tid='%s' and funshion_id='%s'" % (tid, funshion_id)
            print connstr
            
            (code, db_records) = self.fetch_info_with_db(connstr)
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.SUCCESS, rec_dict)

            for rec in db_records:
                rec_dict['tid'] = rec[0]
                rec_dict['uid'] = rec[1]
                rec_dict['ip'] = rec[2]
                rec_dict['port'] = rec[3]
                rec_dict['funshion_id'] = rec[4]
                rec_dict['flag'] = rec[5]
            ret_res = json.dumps(rec_dict)
            return (constant.SUCCESS, ret_res)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_get_video_base_proc.tid: %s, %s" % (tid, e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)
 

    def produce_namespace_info_v2(self, db_records,uid):
        try:
            ret_list = []
            segs_list = ("tid","title","tags","description","priority","channel","step","status","time")
            for rec in db_records:
                rec_dict = {}
                for i in range(0,len(rec)):
                    rec_dict[segs_list[i]] = rec[i]
                rec_dict["uid"] = uid
                rec_dict["time"] = str(rec_dict["time"])
                video_url = ""
                if rec_dict["step"] == "mediaserver" and rec_dict["status"] == 1:
                   video_url = "/audit/redirect_to_msvideo?tid=%s" % rec_dict["tid"]
#                    video_url = "http://%s:80/play/%s/%s.mp4" % (mserver_ip, dat_id, funshion_id)
                rec_dict['video_url'] = video_url
                ret_res = json.dumps(rec_dict)
                ret_list.append(ret_res)
            return ret_list
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in produce_ms_info.%s" % str(e) 
            self.__proc_error.logerror(errinfo)
            return None


    def call_get_forwards_userspace_v2(self, uid, page_size, page, origin="forwards"):
        try:
          
            proc_name = "proc_page_task_v2"
            dbconn = db_connect.DBConnect()
            #ret = dbconn.call_proc_db(proc_name, (page, page_size, uid))
            cursor = dbconn.get_cursor()
            if origin == 'forwards':
                ret = cursor.callproc("proc_page_task_v2",(page,page_size,uid))
            elif origin == 'upload':
                ret = cursor.callproc("proc_upload_video_task",(page,page_size,uid))
            if not cursor:
                return (constant.FAIL, None)
            total = cursor.fetchone()
            total = total[0]
            cursor.nextset()
            page_list = cursor.fetchall()

            map_info = self.produce_namespace_info_v2(page_list,uid)
            if map_info == None:
                return (constant.FAIL, None)
            print 'map_info: ',map_info
            dbconn.close()
            return (constant.SUCCESS,total,map_info)
        except Exception, e:
            print 'call_get_forwards_userspace_v2 exception.', e
            errinfo = "there has exception in call_get_forwards_userspace.uid: %d, %s" % (uid, str(e)) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)

    def call_get_video_msinfo(self,tid):
        try:
            db_mgr = db_connect.DBConnect()
            cursor = db_mgr.get_cursor()
            if not cursor:
                return (constant.FAIL,None)
            tid = tid.encode("utf8")
            proc_name = "proc_get_video_url"
            result = db_mgr.call_proc_db(proc_name, (tid,))
            db_mgr.close()
            return (constant.SUCCESS, result)
        except Exception,e:
            print "exception:",e
            return (constant.FAIL,None)

    def produce_statics_info(self, db_records, time):
        try:
            uid_map = {}
            success_count = 0
            fail_count = 0
            total_count = 0
            staticlist = AuditStaticsList()
            for rec in db_records:
                tid = rec[0]
                uid = rec[1]
                username = rec[2]
                flag = int(rec[3])
                if not uid_map.has_key(uid):
                    staticlist.add_statics_info(uid, username, 0, 0, 0, time) 
                if flag == 0:
                        staticlist.add_fail_num(uid)
                else:
                        staticlist.add_success_num(uid)
                uid_map[uid] = uid
            ret_list = staticlist.to_infolist()
            return ret_list
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in produce_ms_info.%s" % str(e) 
            self.__proc_error.logerror(errinfo)
            return None

    #get the statics info.
    def call_get_audit_statics_info(self, begin_time, end_time, page_size, page):
        try:
            rec_list = []
            cur_page = page
            t_begin_time = "%s 00:00:00" % (begin_time)
            t_end_time = "%s 23:59:59" % (end_time)

            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_statics_audit_info_v2",(cur_page, page_size, t_begin_time, t_end_time))
            if not cursor:
                return (constant.FAIL, 0, None, None)

            users_num = cursor.fetchone()
            users_num = users_num[0]          #审核人员数
            cursor.nextset()
            db_records = cursor.fetchall()
            if len(db_records) == 0:
                print 'None db_records' 
                return (constant.SUCCESS,0,rec_list,rec_list)
            
            for rec in db_records:
                rec_dict={}
                rec_dict['uid'] = rec[0]
                rec_dict['username'] = rec[1]
                rec_dict['success_num'] = rec[2]
                rec_dict['fail_num'] = rec[3]
                rec_dict['total_num'] = rec[4]
                rec_list.append(rec_dict)
            cursor.nextset()
            audit_total_list = cursor.fetchall()
            #audit_total_list = audit_total_list          #统计审核总数 
            print 'total nums:', audit_total_list
            dbconn.close()
            return (constant.SUCCESS, users_num,rec_list, audit_total_list)
        except Exception,e:
            print 'call_get_audit_statics_info has exception, ', e
            self.__proc_error.logerror("call_get_audit_statics_info  error with: %s" % (str(e)))
            return (constant.FAIL, 0, None, None)

    '''
    BEGIN
    START TRANSACTION;

    select uid, username,  
    sum(case when flag = 1 THEN 1 ELSE 0 END) as success_num, 
    sum(case when flag = 0 THEN 1 ELSE 0 END) as fail_num,
    count(*) as total_num
    from ugc_audit_log  
    join auth_user on auth_user.id = ugc_audit_log.uid
    where  time  BETWEEN  i_begin_time and  i_end_time group by uid;

    COMMIT;
    END
    '''
    def call_get_audit_statics_info_v3(self, begin_time, end_time, page_size, page):
        try:
            rec_list = []
            cur_page = page
            t_begin_time = "%s 00:00:00" % (begin_time)
            t_end_time = "%s 23:59:59" % (end_time)

            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_dict_cursor()
            ret = cursor.callproc("proc_statics_audit_info_v3",(cur_page, page_size, t_begin_time, t_end_time))
            if not cursor:
                return (constant.FAIL, 0, None, None)

            db_records = cursor.fetchall()
            users_num = len(db_records)
            audit_total_list = sum([r['total_num'] for r in db_records])

            dbconn.close()
            return (constant.SUCCESS, users_num, db_records, audit_total_list)
        except Exception,e:
            print 'call_get_audit_statics_info has exception, ', e
            self.__proc_error.logerror("call_get_audit_statics_info  error with: %s" % (str(e)))
            return (constant.FAIL, 0, None, None)


    def call_get_audit_statics_num(self, begin_time, end_time):
        try:
            connstr = "select count(DISTINCT(uid))  from v_get_user_audit_info where time BETWEEN  '%s 00:00:00' and '%s 23:59:59'" % (begin_time, end_time)
            (code, db_records) = self.fetch_info_with_db(connstr)
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.SUCCESS, 0)
            count = 0
            for rec in db_records:
                count = rec[0]
            return (constant.SUCCESS, count)
        except Exception,e:
            self.__proc_error.logerror("call_get_audit_statics_num  error with: %s" % (str(e)))
            return None

    def _produce_mp4_details_json(self, page_list):
        try:
            rec_list = []
            for rec in page_list:
                rec_json = {}
                rec_json['funshion_id'] = rec[1]
                rec_json['title'] = rec[2]
                rec_json['site'] = rec[3]
                rec_json['tags'] = rec[4]
                rec_json['file_size'] = rec[5]
                rec_json['file_rate'] = rec[6]
                rec_json['duration'] = rec[7]
                m_ip =  rec[8]
                m_port = rec[9]
                rec_json['origin'] = "%s:%s" % (m_ip, m_port)
                rec_list.append(rec_json)
            return rec_list
        except Exception,e:
            print '_produce_mp4_details_json error', e
            return None


    def call_dat_search_funshionlist(self, key_search, key_type, page_size, page):
        try:
            rec_list = []
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            ret = cursor.callproc("proc_statics_details_info",(key_search, key_type, page, page_size))
            if not cursor:
                return (constant.FAIL, None)
            total = cursor.fetchone()
            total = total[0]
            cursor.nextset()
            page_list = cursor.fetchall()
            if page_list == None:
                print 'None db_records'
                return (constant.SUCCESS, 0,rec_list)
            dbconn.close()
            rec_list = self._produce_mp4_details_json(page_list)
            return (constant.SUCCESS, total, rec_list)
        except Exception,e:
            resean = 'call_dat_search_funshionlist error. %s' % str(e)
            self.__proc_error.logerror("call_dat_search_funshionlist  error with: %s" % (str(e)))
            return (constant.FAIL, None,resean)

    def _produce_dat_statics_json(self, db_records, mp4_total, total):
        try:
            rec_json = {}
            mp4_counter = 0
            dat_send_ok = 0
            dat_send_fail = 0
            mp4_num = 0
            for rec in db_records:
                dat_id = rec[0]
                flag = rec[2]
                mserver_ip = rec[3]
                mserver_port = rec[4]
                if flag == 0:
                    dat_send_fail = dat_send_fail + 1
                else:
                    dat_send_ok = dat_send_ok + 1
            rec_json['dat_success_send'] = str(dat_send_ok)
            rec_json['dat_fail_send'] = str(dat_send_fail)
            rec_json['mp4_total_num'] = str(mp4_total)
            rec_json['dat_total_num'] = str(total)
            return rec_json
        except Exception,e:
            print '_produce_dat_statics_json ', e
            return None

    def call_dat_statics_info(self, begin_time, end_time, page_size, page):
        try:
            rec_list = []
            dbconn = db_connect.DBConnect()
            cursor = dbconn.get_cursor()
            t_begin_time = "%s 00:00:00" % (begin_time)
            t_end_time = "%s 23:59:59" % (end_time)
            ret = cursor.callproc("proc_statics_dat_sort",(t_begin_time, t_end_time, page,page_size))
            if not cursor:
                return (constant.FAIL, None)
            total = cursor.fetchone()
            total = total[0]
            print 'total num: ',total
            cursor.nextset()
            mp4_total = cursor.fetchone()
            mp4_total = mp4_total[0]
            print 'mp4_total num: ', mp4_total
            cursor.nextset()
            page_list = cursor.fetchall()
            if page_list == None:
                print 'None db_records'
                return (constant.SUCCESS, 0,rec_list)
            dbconn.close()
            rec_list = self._produce_dat_statics_json(page_list, mp4_total, total)
            return (constant.SUCCESS, total, rec_list)
        except Exception,e:
            resean =  'call_dat_list_sort error. %s' % str(e)
            print resean
            self.__proc_error.logerror("%s" % (resean))
            return (constant.FAIL, None,resean)

    def call_cloud_get_taskid_bytid(self, tid):
        try:
            rec_dict = {}
            connstr = "select task_id from  ugc_video  where tid='%s'" % (tid)
            print connstr
            (code, db_records) = self.fetch_info_with_db(connstr)
            if code == constant.FAIL:
                return  (constant.FAIL, None)
            elif code == constant.NOT_EXISTS:
                return (constant.SUCCESS, rec_dict)
            task_id = None
            for rec in db_records:
                task_id = rec[0]
            #ret_res = json.dumps(rec_dict)
            return (constant.SUCCESS, task_id)
        except Exception, e:
            print 'exception.', e
            errinfo = "there has exception in call_get_taskid_bytid.tid: %s, %s" % (tid, e) 
            self.__proc_error.logerror(errinfo)
            return (constant.FAIL, None)
