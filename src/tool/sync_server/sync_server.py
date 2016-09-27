#!/usr/bin/python
# -*- coding:utf-8 -*-  

import time
import sys
import logging
import logging.handlers
import os
import MySQLdb

def logger_init():
    logger = logging.getLogger()
    #if etc.DEBUG: 
    logger.setLevel(logging.DEBUG)
    #else:
    #    logger.setLevel(logging.INFO)
    
    log_file = "master.log"
    #handler = logging.handlers.RotatingFileHandler(
    #              etc.LOGPATH + log_file, mode='a', maxBytes=1024*1024*etc.MAX_LOGFILE_SIZE, backupCount=5)
    handler = logging.handlers.RotatingFileHandler(
                  "./server.txt", mode='a', maxBytes=1024*1024*10, backupCount=5)
    #print "Note: log file will be written to " + etc.LOG_DIR + log_file
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

class sync_server:

    def __init__(self):
        self.__ds_ip = "192.168.177.3"#db ip
        self.__ds_port = 3306#db port
        self.__ds_username = "root"#db username
        self.__ds_passworld = "funshion"
        self.__ds_dbname = "ch_old"

        self.__maze_ip = "192.168.177.3"#maze db ip
        self.__maze_port = 3306#maze db port
        self.__maze_username = "root"
        self.__maze_passworld = "funshion"
        self.__maze_dbname = "ugc_test"
        #self.__ds_conn = MySQLdb.connect(host=etc.mysqlip,user=etc.username,db=etc.dbname,passwd=etc.passworld,port=etc.mysqlport,charset="utf8")
        self.__ds_conn = MySQLdb.connect(host=self.__ds_ip,user=self.__ds_username,db=self.__ds_dbname,passwd=self.__ds_passworld,port=self.__ds_port,charset="utf8")
        self.__maze_conn = MySQLdb.connect(host=self.__maze_ip,user=self.__maze_username,db=self.__maze_dbname,passwd=self.__maze_passworld,port=self.__maze_port,charset="utf8")

        self.__ds_cur = self.__ds_conn.cursor()
        self.__maze_cur = self.__maze_conn.cursor()

        self._ds_tb_name = "episode_status"
        self._maze_tb_name = "ugc_video"

        self.__step_id2name = {}
        self.__step_name2id = {}
        mysqlstr = "select step_name,step_id from step"
        try:
            self.__ds_cur.execute(mysqlstr)
            res = self.__ds_cur.fetchall()
            tlen = len(res)
            if tlen != 0:
                for i in range (tlen):
                    (step_name,step_id) = res[i]
                    self.__step_id2name[step_id] = step_name
                    self.__step_name2id[step_name] = step_id
            self.__ds_conn.commit()
        except Exception, e:
            logging.error("select step_name,step_id error : " + str(e))
            sys.exit(1)

    def get_old_status(self):
        mysqlstr = "select id,tid from %s where not (step_id = '60' and status = '1') and not  (status = '2')" % (self._ds_tb_name,)
        para = ()
        #dstatus = {}
        rlist = []
        try:
            self.__ds_cur.execute(mysqlstr,para)
            res = self.__ds_cur.fetchall()
            tlen = len(res)
            if tlen != 0:
                for i in range (tlen):
                    (id,tid) = res[i]
                    dstatus = {}
                    dstatus["id"] = id
                    dstatus["tid"] = tid
                    rlist.append(dstatus)
            self.__ds_conn.commit()
        except Exception, e:
            logging.error("get_old_status error : " + str(e))
        return rlist
            

    def sync_status(self):
        try:
            dstatus = self.get_old_status()
            tlen = len(dstatus)
            for i in range (tlen):
                tdict = dstatus[i]
                id = tdict["id"]
                tid = tdict["tid"]
                (step,status) = self.get_step_status(tid)
                if step :
                    self.update_status(id,step,status)
        except Exception, e:
            logging.error("sync_status error : " + str(e))
        

    def get_step_status(self,tid):
        step = None
        status = None
        try:
            mysqlstr = "select step,status from %s where tid = %%s" % (self._maze_tb_name,)
            para = (tid)
            dstatus = {}
            self.__maze_cur.execute(mysqlstr,para)
            res = self.__maze_cur.fetchall()
            if len(res) != 0:
                (step,status) = res[0]
            self.__maze_conn.commit()
        except Exception, e:
            logging.error("get_step_status error : " + str(e))

        return (step,status)
   

    def update_status(self,id,step_name,status):
        try:
            step_id = self.__step_name2id[step_name]
            mysqlstr = "update %s set step_id = %%s,status = %%s where id = %%s" % (self._ds_tb_name,)
            para = (step_id,status,id)
            self.__ds_cur.execute(mysqlstr,para)
            self.__ds_conn.commit()
        except Exception, e:
            logging.error("update step_id,status error : " + str(e))



def main():
    logger_init()
    server = sync_server()
    while True:
        try:
            server.sync_status()
            time.sleep(15)
        except Exception, e:
            logging.error("whiel True error : " + str(e))
            time.sleep(15)

    #server = http_server.HttpServer()
    #server.start(etc.SERVICE_PORT)

if __name__ == "__main__":
    main()
