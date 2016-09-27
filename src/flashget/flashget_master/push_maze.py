#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
    The thread to synchronize conf from push management server
"""
import logging
import logging.handlers
import time
import threading
import httplib
import urllib2
import json
import os
from task_dao import TaskDao
import etc

class push_maze(threading.Thread):

    _instance_lock = threading.Lock()

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = True
        self.__dict = {}
        self.__list = []
        self.__lock = threading.Lock()
        self.__conn = TaskDao()

    def run(self):
        while True:
            try:
                bempty = self.push_maze()
                if bempty:
                    time.sleep(10)
                    self.load_msg()
                time.sleep(0.1)
            except Exception, err:
                logging.error("run push_maze error" + str(err))

    def push_msg(self,fid,task_id,id,result,url):
        self.__lock.acquire()
        try:
            self.__list.append((fid,task_id,id,result,url))
            logging.info("list size:%d",len(self.__list))
            #self.__dict[task_id] = result
        except Exception, err:
            logging.error("push_msg error" + str(err))
        self.__lock.release()

    def push_maze(self):
        bempty = False
        self.__lock.acquire()
        try:
            tlen = len(self.__list)
            if tlen > 0:
                (fid,task_id,id,result,url) = self.__list.pop()
                tdres = {}
                #tdres["task_id"] = task_id
                tdres["did"] = task_id
                #tdres["url"] = etc.video_url + task_id
                tdres["url"] = url
                tid = []
                tid.append(id)
                tdres["id"] = tid
                tdres["result"] = str(result)
                sres = json.dumps(tdres)
                requrl = "http://" + etc.dataserver_ip +":" + str(etc.dataserver_port) + "/maze/download_finish"
                while True:
                    try:
                        f = urllib2.urlopen(requrl,sres)
                        res = f.read()
                        rjson = json.loads(res)
                        ret = rjson["ret"]
                        logging.info("report to maze ok,task_id:" + task_id + ",result:" + str(result))
                        self.__conn.update_report_status(fid,task_id,1)
                        break
                    except Exception, err:
                        logging.error("report to maze error:" + str(err))
                        time.sleep(10)
            else:
                bempty = True
                logging.info("__list is empty")
        except Exception, err:
            logging.error("get info from list error:" + str(err))
        self.__lock.release()
        return bempty

    def load_msg(self):
       try:
           self.__list = self.__conn.get_sending_msg()
           #print self.__list
       except Exception, err:
            logging.error("load_msg error:" + str(err)) 
                        

if __name__ == "__main__":
    #conf = ConfManager()
    #conf.daemon  = True
    #conf.start()

    id = "0b49884b3b85f7ccddbe4e96e4ae2eae7a6dec56"
    url = "http://125.39.66.178:5050/livestream/3702892333/0b49884b3b85f7ccddbe4e96e4ae2eae7a6dec56/flv/2014/04/29/20131017T171949_03_20140429_191140_4564888.flv"

    #msgcnt.msgcnt.instance()
    #tm = taskmanager.instance()
    #task = taskitem(id,url);
    #tm.add_task(task)
    #task1 = tm.get_task();
    #print task1

    time.sleep(100000)
    
    pass
