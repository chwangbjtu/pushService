#!/usr/bin/python
# -*- coding:utf-8 -*-  

"""Control log function."""

import time
import os.path
import threading
import logging
import logging.handlers
import etc

class tlogger:
    _instance_lock = threading.Lock()
    def __init__(self):
        self.__lock          = threading.Lock()

    @staticmethod
    def instance():
        if not hasattr(tlogger, "_instance"):
            with tlogger._instance_lock:
                if not hasattr(tlogger, "_instance"):
                    # New instance after double check
                    tlogger._instance = tlogger()
        return tlogger._instance

    def writelog(self,task_id,vid,site):
        try:
            f = file(etc.data_file,"w")
            info = task_id + "," + vid + "," + site

            f.write(info)
            f.flush()
            f.close()
        except Exception, err:
            logging.error(str(err))
            logging.error("write data error :" + str(type) + "," + str(id))


    def getlog(self):
        res = (None,None,None)
        try:
            f = file(etc.data_file,"a+")#task_id,vid,site
            linenum = 0
            if True:
                line1 = f.readline()
                line = None
                line = line1.rstrip()
                if line:
                    tline = line.split(",")
                    if len(tline) >= 3:
                        task_id = tline[0]
                        vid = tline[1]
                        site = tline[2]
                        res = (task_id,vid,site)


        except Exception, err:
            logging.error(str(err))

        return res


if __name__ == "__main__":
    tlog = tlogger.instance()
    #tlog.writelog("123","34","asdfasdf")
    #tlog.writelog("1234","344","asdfasdf")
    #tlog.writelog("1234d","344","asdfasdf")
    #tlog.writelog("1234dk","344","asdfasdf")
    #tlog.writelog("1234dk1","344","asdfasdf")
    tlog.getlog()
