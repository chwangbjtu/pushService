#!/usr/bin/python
# -*- coding:utf-8 -*-

import task
import maze_service
import logging
import state_machine

class RequireTask(task.Task):
    def __init__(self,cb_func):
        task.Task.__init__(self,cb_func)

    def pack_map_obj(self):
        return None

    def execute(self,count):
        ret,msg = maze_service.require_task(count,self._handle_recv_task)
        if ret:
            logging.debug("tasks are requested from maze, set pending to true")
            state_machine.cycle.add_conn()
            state_machine.cycle.set_pending()
        else:
            logging.info("can not request any tasks from maze")

    def _handle_recv_task(self,res,message):
        logging.debug("response of requesting task from maze received, set pending state, of state machine's cycle, to false")
        self._cb_func(res,message,self)
        state_machine.cycle.set_pending(False)

class ReportCloudIDTask(task.Task):
    def __init__(self,cb_func,tid,cloud_id):
        task.Task.__init__(self,cb_func)
        self.__tid = tid
        self.__cloud_id = cloud_id

    def tid(self):
        return self.__tid

    def cloud_id(self):
        return self.__cloud_id

    def pack_map_obj(self):
        return {"tid":self.__tid,"cloud_id":self.__cloud_id}

    def execute(self,args):
        if state_machine.cycle.exiting():
            logging.debug("add report cloud id task to state machine's cycle")
            state_machine.cycle.add_task(self)
        logging.debug("report to maze with cloud id %s", self.__cloud_id)
        ret,err_msg =  maze_service.report_cloud_id(self.__tid,self.__cloud_id,self._handle_report_id)
        if ret:
            state_machine.cycle.add_conn()
        else:
            state_machine.cycle.add_task(self)
            logging.info("can not report to maze with cloud id %s with err: %s", self.__cloud_id, err_msg)
        
    def _handle_report_id(self,ret,args):
        logging.debug("response of reporting cloud id task received")
        return self._cb_func(ret,args,self)
