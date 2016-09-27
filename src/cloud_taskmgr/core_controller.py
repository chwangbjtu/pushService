#!/usr/bin/python
# -*- coding:utf-8 -*-

import json
import tornado.ioloop
import tornado.httpclient
import state_machine
import config_loader
import logging
import task
import maze_task
import cloud_task
import error
import state_machine
import taskstg

def get_maze_task(count):
    job = maze_task.RequireTask(_handle_task_list)
    job.execute(count)

def _handle_task_list(success,args,cur_job):
    if not success:
        code,err_msg = (args[0],args[1])
        logging.info("error when requesting task list from maze: %s", err_msg)
    else:
        tasklist = args
        logging.debug("%d tasks from maze, execute one by one", len(tasklist))
        for item in tasklist:
            job = cloud_task.CloudTask(_handle_recv_cloud_id,item)
            job.execute(None)
        state_machine.cycle.add_task_ref(len(tasklist))
    state_machine.cycle.sub_conn()
     
def _handle_recv_cloud_id(success,args,cloud_job):
    if success:
        cloud_id = args
        logging.debug("create one report for cloud id task with tid %s and cloud id %s", cloud_job.tid(), cloud_id)
        job = maze_task.ReportCloudIDTask(_handle_recv_report_cloud, cloud_job.tid(), cloud_id)
        job.execute(None)
    else:
        code,err_msg = (args[0],args[1])
        if error.match(code,error.ERROR_HTTP_REQUEST_TIMEOUT):
            state_machine.cycle.add_task(cloud_job)
        else:
            state_machine.cycle.sub_task_ref()
        logging.info("failed to receive cloud id message")
    state_machine.cycle.sub_conn()
        
def _handle_recv_report_cloud(success,args,maze_report_job):
    if success:
        state_machine.cycle.sub_task_ref()
        logging.debug("receive response from maze for report cloud message with tid %s and cloud id %s", maze_report_job.tid(), maze_report_job.cloud_id())
    else:
        code,err_msg = (args[0],args[1])
        if error.match(code,error.ERROR_HTTP_REQUEST_TIMEOUT):
            state_machine.cycle.add_task(maze_report_job)
        else:
            state_machine.cycle.sub_task_ref()
        logging.info("failed to receive report cloud message")
    state_machine.cycle.sub_conn()

def flush_task():
    cycle = state_machine.cycle
    tasklist = cycle.get_all_task()
    filename = config_loader.get_record_file()
    stg = taskstg.TaskStg(filename)
    return stg.save_tasklist(tasklist)

def load_task():
    filename = config_loader.get_record_file()
    stg = taskstg.TaskStg(filename)
    ret,tasklist = stg.load()
    if not ret or not tasklist:
        return ret
    cycle = state_machine.cycle
    for job in tasklist:
        cycle.add_task(job)
        cycle.add_task_ref
    return True
