# -*- coding:utf-8 -*-
import time
import logging
import logging.handlers
import threading
from db_connect import MysqlConnect
import traceback

class TaskDao(object):
    def __init__(self, db_conn=None):
        self.__lock = threading.Lock()
        if not db_conn:
            db_conn = MysqlConnect()
        self._db_conn = db_conn
        self._tb_name = 'tasktable'
        self._info_tb_name = 'send_info'
        self._userver_tb_name = 'userver'
        self._upload_info_tb_name = 'upload_info'

    def get_task(self,op,site,worker_ip):
        self.__lock.acquire()
        task_id = None
        vid = None
        url = None
        try:
            if site:
                mysqlstr = "select task_id,vid,src_url from %s where op = %%s and status= %%s and site=%%s order by priority desc limit 1" % (self._tb_name,)
                para = (op,"0",site,)
            else:
                mysqlstr = "select task_id,site,vid,src_url from %s where op = %%s and status= %%s and site != %%s order by priority desc limit 1" % (self._tb_name,)
                para = (op,"0","youtube",)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                if site:
                    (task_id,vid,url) = res[0]
                else:
                    (task_id,tsite,vid,url) = res[0]
                    site = tsite
                #logging.info("find taskid:" + task_id + ", site:" + site+",vid:" + vid)
                logging.info("find taskid: %s,site: %s,vid: %s" , str(task_id),str(site),str(vid))
                mysqlstr = "update %s set status = %%s,worker_ip = %%s where task_id = %%s" % (self._tb_name,)
                para1 = ("1",worker_ip,task_id,)
                self._db_conn.execute_sql(mysqlstr,para1)
                self._db_conn.commit()
        except Exception, e:
            logging.error("get_task error : %s " % traceback.format_exc())
        self.__lock.release()
        return (task_id,site,vid,url)

    def is_taskid_in_db(self,task_id):
        bres = False
        try:
            mysqlstr = "select site from %s where task_id = %%s" % (self._tb_name,)
            para = (task_id,)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                bres = True
            return bres
        except Exception, e:
            logging.error("select site error : " + str(e))
        return bres

    def insert(self,task_id,id,site,vid,priority,op,src_url):
        self.__lock.acquire()
        status = "0"
        url = ""
        try:
            if self.is_taskid_in_db(task_id):
                #tstatus = self.get_status(task_id)
                (url,tstatus) = self.get_msg(task_id)
                status = str(tstatus)
                logging.info("task_id : %s is in db",task_id)
                if int(tstatus) ==  2:#2 is fail,3 si succ
                    mysqlstr = "update %s set status = %%s where task_id = %%s" % (self._tb_name,)
                    para = ("0",task_id,)
                    self._db_conn.execute_sql(mysqlstr,para)
                    self._db_conn.commit()
                    status = "0"
                    logging.info("")
            else:
                logging.info("task_id : %s should inert into db",task_id)
                status = "0"
                url = ""
                mysqlstr = "insert into %s (task_id,id,site,vid,priority,op,status,url,src_url,create_time) values(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s )" % (self._tb_name,)
                now = int(time.time())
                timeArray = time.localtime(now)
                create_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

                logging.info("")
                para = (task_id,id,site,vid,priority,op,status,url,src_url,create_time,)
                self._db_conn.execute_sql(mysqlstr,para)
                self._db_conn.commit()
                logging.info("")
            #insert info to send_info table
            mysqlstr = "insert into %s (id,task_id,status,url) values(%%s,%%s,%%s,%%s)" % (self._info_tb_name,)
            para = (id,task_id,status,url,)
            logging.info("")
            self._db_conn.execute_sql(mysqlstr,para)
            sql = "SELECT LAST_INSERT_ID() from %s" % (self._info_tb_name, )
            res = self._db_conn.db_fetchall(sql)
            self._db_conn.commit()
            logging.info("")
        except Exception, e:
            logging.error("insert error task_id is:" + task_id + ",errinfo is:" + str(e))
        self.__lock.release()
        did = ""
        if res:
            did =  str(res[0][0])
        return did

    def get_status(self,task_id):
        status = None
        try:
            mysqlstr = "select status from %s where task_id = %%s" % (self._tb_name,)
            para = (task_id,)
            logging.debug("mysqlstr:" + mysqlstr)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                status = res[0][0]
            return status
        except Exception, e:
            logging.error("select status from tasktable error : " + str(e))
        return status

    def get_fid(self,task_id):
        fids = []
        try:
            mysqlstr = "select fid from %s where task_id = %%s" % (self._info_tb_name,)
            para = (task_id,)
            logging.debug("mysqlstr:" + mysqlstr)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                tlen = len(res)
                for i in range(tlen):
                    fids.append(res[i][0])
            return fids
        except Exception, e:
            logging.error("select status from tasktable error : " + str(e))
        return fids

    def get_msg(self,task_id):
        url = None
        status = None
        try:
            mysqlstr = "select url,status from %s where task_id = %%s" % (self._tb_name,)
            para = (task_id,)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                (url,status) = res[0]
            return (url,status)
        except Exception, e:
            logging.error("select url,status from tasktable error : " + str(e))

        return (url,status)

    def get_new_msg(self,task_id):
        fid = None
        id = None
        tlist = []
        try:
            mysqlstr = "select fid,id  from %s where task_id = %%s and report_status = %%s" % (self._info_tb_name,)
            para = (task_id,"0",)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                tlen = len(res)
                for i in range(tlen):
                    #(fid,id) = res[i]
                    tlist.append(res[i])
            return tlist
        except Exception, e:
            logging.error("select fid,id from tasktable error : " + str(e))

        return tlist

    def update_db(self,task_id,status,url):
        self.__lock.acquire()
        istatus = int(status)
        try:
            old_status = self.get_status(task_id)
            if not old_status:
                old_status = '0'
            iold_status = int(old_status)
            if istatus > iold_status:
                now = int(time.time())
                timeArray = time.localtime(now)
                download_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

                mysqlstr = "update %s set status = %%s,url = %%s,download_time = %%s where task_id = %%s" % (self._tb_name,)
                para = (str(status),url,download_time,task_id,)
                self._db_conn.execute_sql(mysqlstr,para)
                self._db_conn.commit()
                
                #update send_info
                mysqlstr = "update %s set status = %%s,url = %%s,update_time = %%s where task_id = %%s" % (self._info_tb_name,)
                para = (str(status),url,download_time,task_id)
                self._db_conn.execute_sql(mysqlstr,para)
                self._db_conn.commit()
        except Exception, e:
            logging.error("update_db error task_id is:" + task_id + "errinfo is:" + str(e))
        self.__lock.release()

    def get_report_status(self,fid):
        status = None
        try:
            mysqlstr = "select report_status from %s where fid = %%s" % (self._info_tb_name,)
            para = (fid,)
            logging.debug("mysqlstr:" + mysqlstr)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            if res and len(res) != 0:
                status = res[0][0]
            return status
        except Exception, e:
            logging.error("select report_status from tasktable error : " + str(e))
        return status

    def update_report_status(self,fid,task_id,report_status):
        self.__lock.acquire()
        ireport_status = int(report_status)
        try:
            old_report_status = self.get_report_status(fid)
            if not old_report_status:
                old_report_status = '0'
            iold_report_status = int(old_report_status)

            if ireport_status > iold_report_status:
                now = int(time.time())
                timeArray = time.localtime(now)
                report_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

                #mysqlstr = ("update tasktable set report_status = %d where task_id = \"%s\" ;") % (status,task_id)
                mysqlstr = "update %s set report_status = %%s,update_time = %%s where fid = %%s" % (self._info_tb_name,)
                para = (str(report_status),report_time,fid,)
                self._db_conn.execute_sql(mysqlstr,para)
                self._db_conn.commit()
                logging.info("update tasktable ok,task_id is:" + task_id + ",report_status is:" + str(report_status))
            else:
                logging.warning("update report_status err,old report_status is:" + str(old_report_status) + ",now report_status is:" + str(report_status))
        except Exception, e:
            logging.error("update_report_status error task_id is:" + task_id + "errinfo is:" + str(e))
        self.__lock.release()

    def get_server(self,op):
        ip = None
        port = None
        self.__lock.acquire()
        try:
            mysqlstr = "select ip,port from %s limit 1" % (self._userver_tb_name,)
            res = self._db_conn.db_fetchall(mysqlstr)
            self._db_conn.commit()
            tlen = 0
            tlen = len(res)
            if tlen > 0:
                (ip,port) = res[0]
        except Exception, e:
            logging.error("get_server error"  + "errinfo is:" + str(e))
        self.__lock.release()

        return (ip,port)

    def get_url(self,taskid):
        url = None
        self.__lock.acquire()
        try:
            mysqlstr = "select url from %s where taskid = %%s" % (self._upload_info_tb_name,)
            para = (taskid,)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            tlen = 0
            tlen = len(res)
            if tlen > 0:
                (url) = res[0][0]
        except Exception, e:
            logging.error("get_server error"  + "errinfo is:" + str(e))
        self.__lock.release()

        return (url)

    def is_taskid_in_uploaded(self,taskid):
        is_in_table  = False
        uid = None
        try:
            mysqlstr = "select * from %s where taskid = %%s" % (self._upload_info_tb_name,)
            para = (taskid,)
            logging.info("mysql %s", mysqlstr)
            logging.info("para :" + str(para))
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()
            tlen = 0
            tlen = len(res)
            logging.info("num :" + str(tlen))
            if tlen > 0:
                #uid = res[0]
                is_in_table = True
                logging.info("is_in_table true")
        except Exception, e:
            logging.error("is_taskid_in_uploaded error"  + "errinfo is:" + str(e))

        return is_in_table

    def upload_start(self,taskid,file_name,file_size,file_url,uid,hashid):
        self.__lock.acquire()
        try:
            now = int(time.time())
            timeArray = time.localtime(now)
            create_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))

            if self.is_taskid_in_uploaded(taskid):
                logging.info("")
                #mysqlstr = "update %s set status = %%s,last_time = %%s where taskid = %%s" % (self._upload_info_tb_name,)
                #para = ("3",create_time,taskid,)
                pass
            else:
                mysqlstr = "insert into %s (uid,hashid,taskid,filename,length,status,create_time,last_time) values(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s )" % (self._upload_info_tb_name,)
                para = (uid,hashid,taskid,file_name,file_size,"0",create_time,create_time,)
                #para = (uid,hashid,taskid,file_name,file_size,)
                self._db_conn.execute_sql(mysqlstr,para)
                self._db_conn.commit()
        except Exception, e:
            logging.error("upload_start error"  + "errinfo is:" + str(e))
        self.__lock.release()

    def upload_finish(self,taskid,file_name,file_size,file_url,uid,hashid):
        self.__lock.acquire()
        try:
            now = int(time.time())
            timeArray = time.localtime(now)
            create_time = str(time.strftime("%Y-%m-%d %H:%M:%S", timeArray))
            if self.is_taskid_in_uploaded(taskid):
                logging.info("")
                #mysqlstr = "replace into %s (uid,hashid,taskid,filename,length,url,status,last_time) values(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s )" % (self._upload_info_tb_name,)
                mysqlstr = "update %s set status = %%s,url = %%s,last_time = %%s where taskid = %%s" % (self._upload_info_tb_name,)
                para = ("3",file_url,create_time,taskid,)
                
            else:
                mysqlstr = "insert into %s (uid,hashid,taskid,filename,length,url,status,last_time) values(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s )" % (self._upload_info_tb_name,)
                para = (uid,hashid,taskid,file_name,file_size,file_url,"3",create_time,)
                #para = (uid,hashid,taskid,file_name,file_size,)
            self._db_conn.execute_sql(mysqlstr,para)
            self._db_conn.commit()
        except Exception, e:
            logging.error("upload_finish error"  + "errinfo is:" + str(e))
        self.__lock.release()

    def get_sending_msg(self):
        tlist = []
        try:
            mysqlstr = "select fid,task_id,id,status,url from %s where report_status = %%s and status > %%s" % (self._info_tb_name,)
            para = ("0","1",)
            res = self._db_conn.db_fetchall(mysqlstr,para)
            self._db_conn.commit()

            tlen = 0
            if res:
                tlen = len(res)
            if tlen != 0:
                for i in range (tlen):
                    (fid,task_id,id,status,url) = res[i]
                    logging.info("get_sending_msg fid is:%s,task_id is:%s,id is:%s,status is:%s,url is:%s",fid,task_id,str(id),str(status),str(url))
                    rstatus = "1"
                    if status == "3":
                        rstatus = "0"
                    tlist.append((fid,task_id,id,rstatus,url))
            logging.info("get_sending_msg size:" + str(len(tlist)))
        except Exception, e:
            logging.error("get_sending_msg from tasktable error : " + str(e))
        return tlist

if __name__ == "__main__":

    try:
        db_conn = MysqlConnect()
        task_dao = TaskDao(db_conn)

        '''
        res = task_dao.get_last_update_time()
        log.app_log.debug('service last update: %s' % (res, ))
        db_conn.commit()

        task = {'data_count': 10, 'begin_time': '2014-06-05 16:00:00', 'end_time': '2014-06-05 16:15:10'}
        task_dao.insert_task(task)
        task_id = task_dao.get_last_insert_task()
        task['task_id'] = task_id
        task_dao.update_task(task)
        '''

    except Exception,e:
        #log.app_log.error(traceback.format_exc())
        logging.error(str(e))

