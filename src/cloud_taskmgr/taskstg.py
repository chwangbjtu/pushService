#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import logging
import utils
import task
import os

class TaskStg(object):
    def __init__(self,filename):
        self.__filename = filename

    def load(self):
        try:
            logging.critical("load task store from %s ... ", self.__filename)
            if not os.path.exists(self.__filename):
                return (True,None)
            handler = open(self.__filename,"r")
            json_str = handler.read()
            if not json_str:
                return (True,None)
        except Exception,e:
            logging.critical("exception when loading task store from %s, %s", self.__filename, str(e))
            return (False,None)
        try:
            task_list = []
            task_map_list = json.loads(json_str)
            for item in task_map_list:
                task_obj = task.Task(item)
                if task_obj.tid != None:
                    task_list.append(task_obj)
                else:
                    logging.info("wrong task parameter with vid %s", task_obj.vid[1])
        except Exception,e:
            handler.close()
            logging.critical("exception when paring task from %s, %s", self.__filename, str(e))
            return (False,None)
        return (True,task_list)

    def save_tasklist(self,tasklist):
        task_map_list = []
        for item in tasklist:
            task_map_obj = item.pack_map_obj()
            task_map_list.append(task_map_obj)
        try:
            json_str = json.dumps(task_map_list)
        except Exception,e:
            logging.critical("exception when dumping task map", str(e))
            return False
        try:
            logging.info("store task map to %s ... ", self.__filename)
            file_handler = None
            file_handler = open(self.__filename, "w")
            file_handler.write(json_str)
        except Exception,e:
            logging.critical("exception when storing task map to %s, %s", self.__filename, str(e))
            if file_handler:
                file_handler.close()
            return False
            file_handler.close()
        return True
        

if __name__ == "__main__":
    task_obj = task.Task()
    task_obj.tid = "X12312545234"
    task_obj.vid = "XLDKFE8223"
    task_obj.site = "yk"
    task_obj.priority = 4
    task_list = [task_obj,]
    stg = TaskStg("tasklist.dat")
    ret = stg.save_tasklist(task_list)
    print "save task list : %s" % str(ret)
    ret,task_list = stg.load()
    print "load task : %s" % str(ret)
    if ret:
        for item in task_list:
            print item.pack_json_str()
    raw_input("press")

