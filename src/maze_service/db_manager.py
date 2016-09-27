#!/bin/env python
# -*- coding: utf-8    -*-
import logging
import MySQLdb
import json
import time

import constant
import db_connect

class DBManager:
    def __init__(self):
        pass
    # new vides from spider, upload, forward or push 
    def add_video_task(self, task):
        result = {}
        result["result"] = False
        dbconn = db_connect.DBConnect()
        try:
            tid         = task['tid']
            uid         = task['uid']
            vid         = task['vid']
            site        = task['site']
            title       = task['title']
            describe    = task['describe']
            tags        = task['tags']
            channel     = task['channel']
            origin      = task['origin']
            priority    = task['priority']
            pub_time    = str(task['pub_time'])
            audit_free  = task['audit_free']
            
            proc_name = "proc_add_video_task"
            logging.debug("call stored procedure [%s]", proc_name)            
            (code, ret) = dbconn.call_proc_db(proc_name, (tid, uid, vid, site, MySQLdb.escape_string(title), MySQLdb.escape_string(describe), MySQLdb.escape_string(tags), channel, origin, priority, pub_time, audit_free))
            
            if code != constant.SUCCESS:
                logging.info("failed to call stored procedure %s with tid: %s, error:%s", proc_name, tid, ret)
                return result
            result['result'] = True
            result['tid'] = tid
            return result
        except Exception, err:
            logging.warning("exception when calling stored procedure %s", str(err))
            return  result
        finally:
            dbconn.close()
    
    # task id (or cloud_id) is used to match video     
    def add_taskid_tid(self, task):
        dbconn = db_connect.DBConnect()
        try:
            cloud_id  = task['cloud_id']
            tid       = task["tid"]
            proc_name = 'proc_add_taskid_tid'
            (code, db_records) = dbconn.call_proc_db(proc_name, (tid, cloud_id))
            
            if code != constant.SUCCESS:
                logging.info("failed to call stored procedure %s with tid: %s, cloud_id:%s, error:%s", proc_name, tid, cloud_id, db_records)
                return {"result": False}
            
            logging.debug("report cloudid-tid: %s-%s", cloud_id, tid)
            return {"result": True}
        except Exception, err:
            logging.warning('exception when call stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
    
    # transcode result 
    def _format_transcode_list(self, task):
        value_list = []
        for transcode in task["transcode"]:
            ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            #db-fields: funshion_id, tid, rate, file_size, filename, duration, video_url, small_image, large_image, ctime, definition
            str_temp = "'%s', '%s', '%s', %ld, '%s', %ld, '%s', '%s','%s',  '%s', '%s'" % (transcode["funshion_id"], task["tid"], transcode["rate"], long(transcode["size"]), transcode["filename"],  long(transcode["milliseconds"]),  transcode["video_url"], transcode["small_image"], transcode["large_image"], ctime, transcode["definition"])
            value_list.append(str_temp)
        return self._format_value_list(value_list)
        
    def add_transcode_report(self, task):
        dbconn = db_connect.DBConnect()
        try:
            tid = task["tid"]
            values_str = self._format_transcode_list(task)
            proc_name = 'proc_add_transcode_report'

            (ret, res) = dbconn.call_proc_db(proc_name, (task["tid"], values_str, "0", "0"))
            if ret != constant.SUCCESS:
                logging.info("failed to call stored procedure %s. with tid: %s, error:%s", proc_name, tid, res)
                return {"result": False}
            
            logging.debug("cloud_transcode_report: %s", values_str)
            return {"result": True}
        except Exception, err:
            logging.warning("exception when processing transcode report %s\n%s", str(err), json.dumps(task))
            return {"result": False}
        finally:
            dbconn.close()
            
    def set_transcode_fail(self, task):
        dbconn = db_connect.DBConnect()
        try:
            proc_name = 'proc_set_transcode_fail'

            cursor = dbconn.get_cursor()
            cursor.callproc(proc_name,(task['tid'],))
            if not cursor:
                return {"result": False}

            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
    
    # package result 
    def set_package_start(self, task):
        dbconn = db_connect.DBConnect()
        
        try:
            proc_name = 'proc_set_package_start'

            cursor = dbconn.get_cursor()
            cursor.callproc(proc_name,(task['tid'],))
            if not cursor:
                return {"result": False}

            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
            
    def _format_value_list(self, value_list):
        sql_sentence = ""
        if len(value_list) == 0:
            return  sql_sentence
        for seg in value_list:
            if sql_sentence:
                sql_sentence += ","
            if isinstance(seg, str) or isinstance(seg, unicode):
                sql_sentence += "(%s)" % (seg)
            else:
                sql_sentence += "(%s)" % str(seg)
        return sql_sentence
        
    def audit_video_task(self, task):    
        dbconn = db_connect.DBConnect()
        try:
            base_info_sql = ""
            audit_info_sql = ""
            result = 1 if task['pass'] else 0
            if task['pass']:
                base_info_sql  = 'title="%s", channel="%s", tags = "%s", description="%s"' % (MySQLdb.escape_string(task['title']), task['channel'], MySQLdb.escape_string(task['tags']), MySQLdb.escape_string(task['description']))
                audit_info_sql   = 'logo="%s"' % task['logo']
                
            proc_name = "proc_audit_video_task_v2"
            cursor = dbconn.get_cursor()
            if not cursor:
                logging.warning("can not get db cursor ... ")
                return {"result": False}
            cursor.callproc(proc_name, (task['uid'], task['tid'], task['fid'], result, base_info_sql, audit_info_sql))
            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
            
    def _format_package_list(self, task):
        value_list = []
        for tid in task['tid']:
            str_temp = "'%s', '%s'" % (task['infohash'], tid)
            value_list.append(str_temp)
        return self._format_value_list(value_list)
        
    def add_package_report(self, task):
        dbconn = db_connect.DBConnect()
        try:
            proc_name = 'proc_add_package_report'
            dat_id       = task['infohash']
            dat_size     = task['size']
            mserver_ip   = task['server_ip']
            mserver_port = task['server_port']
            
            logging.debug("call stored procs %s", proc_name)
            package_valuse = self._format_package_list(task)
            tid_values = "(" + self._format_tid_list(task) + ")"
            cursor = dbconn.get_cursor()
            if not cursor:
                logging.warning("can not get db cursor ... ")
                return {"result": False}
            cursor.callproc(proc_name,(dat_id, dat_size, mserver_ip, mserver_port, package_valuse, tid_values))

            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
            
    def _format_tid_list(self, task):
        value_list = []
        for tid in task['tid']:
            str_temp = "'%s'" % tid
            value_list.append(str_temp)
        return self._format_value_list(value_list)
        
    def set_package_fail(self, task):
        dbconn = db_connect.DBConnect()
        try:
            proc_name = 'proc_set_package_fail'
            tid_values = "(" + self._format_tid_list(task) + ")"
            cursor = dbconn.get_cursor()
            if not cursor:
                return {"result": False}
            cursor.callproc(proc_name,(tid_values,))
            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
    
    def set_distribute_start(self, task):
        dbconn = db_connect.DBConnect()
        
        try:
            proc_name = 'proc_set_distribute_start'
            tid_values = "(" + self._format_tid_list(task) + ")"
            cursor = dbconn.get_cursor()
            
            cursor.callproc(proc_name,(task['infohash'], tid_values, ))
            if not cursor:
                return {"result": False}

            return {"result": True}
        except Exception, err:
            logging.warning('exception when calling stored procedure: %s', str(err))
            return {"result": False}
        finally:
            dbconn.close()
            
    # videos in ugc_video    
    def _produce_all_videolist(self, db_records, all_video_map):
        for rec in db_records:
            #select tid, task_id, uid, priority, audit_free, step, status, vid, title, tags, channel, description, site from ugc video where status != 2
            rec_json = {}
            rec_json['tid']        = rec[0]
            rec_json['cloud_id']   = rec[1]
            rec_json['uid']        = rec[2]
            rec_json['priority']   = rec[3]
            rec_json['audit_free'] = rec[4]
            rec_json['step']       = rec[5]
            rec_json['status']     = rec[6]
            rec_json['vid']        = rec[7]
            rec_json['title']      = rec[8]
            rec_json['tags']       = rec[9]
            rec_json['channel']     = rec[10]
            rec_json['description'] = rec[11]
            rec_json['site']        = rec[12]
            
            all_video_map[rec_json['tid']] = rec_json

    def load_all_videos(self): # task_id in ugc_video table MUST be re-defined
        all_videos_map = {}
        dbconn = db_connect.DBConnect()
        try:
            connstr = '''select tid, task_id, uid, priority, audit_free, step, status, vid, title, tags, channel, description, site from ugc_video where status != 2'''
            
            db_records = dbconn.db_fetchall(connstr)
            if not db_records:
                return all_videos_map
            self._produce_all_videolist(db_records, all_videos_map)
            return all_videos_map
        except Exception, err:
            logging.warning('exception when loading videos from ugc_video: %s ', str(err))
            return all_videos_map
        finally:
            dbconn.close()
    
    # files in ugc_file     
    def _produce_transcode_filelist(self, db_records, transcode_file_map):
        #connstr = "select  tid, filename, file_size, funshion_id, rate, duration, definition, small_image, logo from ugc_file where tid ='%s'" % (tid)
        for rec in db_records:
            video_json = {}
            tid                        = rec[0]
            video_json['filename']     = rec[1]
            video_json['file_size']    = rec[2]
            video_json['funshion_id']  = rec[3]
            video_json['rate']         = rec[4]
            video_json['duration']     = rec[5]
            video_json['definition']   = str(rec[6])
            video_json['small_image']  = rec[7]
            video_json['logo']         = rec[8]
            if not transcode_file_map.has_key(tid):
                transcode_file_map[tid] = [video_json]
            else:
                transcode_file_map[tid].append(video_json)
                            
    def load_transcode_files(self):
        dbconn = db_connect.DBConnect()
        transcode_file_map = {}
        try:
            connstr = '''select  tid, filename, file_size, funshion_id, rate, duration, definition, small_image, logo from ugc_file;'''
            db_records = dbconn.db_fetchall(connstr)
            if not db_records:
                return transcode_file_map
            self._produce_transcode_filelist(db_records, transcode_file_map)
            return transcode_file_map
        except Exception, err:
            logging.warning('exception when loading transcode files from ugc_file: %s ', str(err))
            return transcode_file_map
        finally:
            dbconn.close()
    
    # dat files in ugc_dat    
    def _produce_distribute_tasklist(self, db_records, distribute_task_map):
        for rec in db_records:
            dat_json = {}
            if not distribute_task_map.has_key(rec[0]):
                dat_json['infohash']    = rec[0]
                dat_json['size']        = rec[1]
                dat_json['ip']          = rec[2]
                dat_json['port']        = rec[3]
                dat_json['flag']        = rec[4]
                dat_json["tid"]         = {rec[5]:rec[5]} 
                distribute_task_map[rec[0]] = dat_json
            else:
                dat_json = distribute_task_map[rec[0]]
                dat_json["tid"][rec[5]] = rec[5]
                            
    def load_distribute_tasks(self):
        dbconn = db_connect.DBConnect()
        distribute_task_map = {}
        try:
            connstr = '''select `ugc_dat`.`dat_id` AS `dat_id`,
                                `ugc_dat`.`dat_size` AS `dat_size`,
                                `ugc_dat`.`mserver_ip` AS `mserver_ip`,
                                `ugc_dat`.`mserver_port` AS `mserver_port`,
                                `ugc_dat`.`flag` AS `flag`,
                                `ugc_fid_map`.`tid` AS `tid`    
                         from `ugc_fid_map` join `ugc_dat`  
                         where `ugc_dat`.`dat_id` = `ugc_fid_map`.`dat_id`;'''
            
            db_records = dbconn.db_fetchall(connstr)
            if not db_records:
                return distribute_task_map
            self._produce_distribute_tasklist(db_records, distribute_task_map)
            return distribute_task_map
        except Exception, err:
            logging.warning('exception when loading distribute tasks from ugc_dat: %s ', str(err))
            return distribute_task_map
        finally:
            dbconn.close()

    def _produce_auth_users(self, db_records, auth_users_map):
        for rec in db_records:
            auth_users_map[rec[0]]    = rec[1]
   
    def load_auth_users(self):
        dbconn = db_connect.DBConnect()
        auth_users_map = {}
        try:
            connstr = '''select id, username from auth_user;'''
            db_records = dbconn.db_fetchall(connstr)
            if not db_records:
                return auth_users_map
            self._produce_auth_users(db_records, auth_users_map)
            auth_users_map["result"] = True
            return auth_users_map
        except Exception, err:
            logging.warning('exception when loading distribute tasks from ugc_dat: %s ', str(err))
            auth_users_map["result"] = False
            return auth_users_map
        finally:
            dbconn.close()
            
if __name__ == "__main__":
    manager = DBManager()
    manager.load_all_videos()
    manager.load_transcode_files()
    manager.load_distribute_tasks()

