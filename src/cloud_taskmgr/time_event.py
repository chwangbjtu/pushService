#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import tornado.ioloop
import state_machine
import taskstg
import logging
import core_controller
import config_loader

def post_start_event():
    if not core_controller.load_task():
        logging.info("does not Load any task from record")
    loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time()
    timeout = loop.add_timeout(deadline,timeout_handler)
    logging.debug("wait for the next round at %s", str(deadline))
    state_machine.cycle.set_timeout(timeout)

def _process_exiting():
    cycle = state_machine.cycle
    if cycle.conn() > 0:
        logging.debug("cycle.conn() > 0 ...")
        return
    core_controller.flush_task()
    loop = tornado.ioloop.IOLoop.instance()
    loop.stop()
    logging.info("prepare to quit when cycle.conn() = 0")

def timeout_handler():
    cycle = state_machine.cycle
    loop = tornado.ioloop.IOLoop.instance()
    if cycle.exiting():
        logging.debug("prepare to quit when no cycle.conn() = 0")
        return _process_exiting()
    #post the cached task
    while True:
        task_obj = cycle.get_task()
        if not task_obj:
            logging.debug("no task found in state machine's cycle")
            break
        logging.debug("execute task found in state machine's cycle")
        task_obj.execute(None)
    if not cycle.pending(): 
        #ask for more task from maze
        logging.debug("no any task pending in state machine's cycle")
        max_task_count = config_loader.get_max_task_count()
        count = max_task_count - cycle.task_count()
        if count > 0:
            logging.debug("request %d tasks from maze", count)
            core_controller.get_maze_task(count)
    #reset polling
    time_interval = config_loader.get_time_interval()
    loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + time_interval
    timeout = loop.add_timeout(deadline,timeout_handler)
    logging.debug("wait for the next round at %s", str(deadline))
    state_machine.cycle.set_timeout(timeout)