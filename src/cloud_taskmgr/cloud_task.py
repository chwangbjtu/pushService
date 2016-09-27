#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import error
import task
import cloud_service
import logging
import state_machine

class CloudTask(task.Task):
    def __init__(self,cb_func,arg_map=None):
        task.Task.__init__(self,cb_func)
        self.__task = arg_map

    def tid(self):
        if self.__task.has_key("tid"):
            return self.__task["tid"]
        return None

    def pack_json_str(self):
        return json.dumps(self.__task)

    def pack_map_obj(self):
        return self.__task

    def execute(self,args):
        if state_machine.cycle.exiting():
            state_machine.cycle.add_task(self)
            return
        vid = self.__task["vid"]
        logging.debug("post task vid %s to cloud service \n%s", vid, json.dumps(self.__task))
        ret,err_msg = cloud_service.post_task2(self.__task, self._handler_cloud_response)
        if not ret:
            logging.info("can not post task to cloud service with tid %s: %s", self.__task["tid"], err_msg[1])
            state_machine.cycle.add_task(self)
        else:
            logging.debug("increase one connection to state machine's cycle")
            state_machine.cycle.add_conn()

    def _handler_cloud_response(self,ret,message):
        logging.debug("response received from cloud service %s", ret)
        return self._cb_func(ret,message,self)
