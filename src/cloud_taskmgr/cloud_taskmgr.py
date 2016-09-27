#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import sys
import config_loader
import tornado.ioloop
import taskmgr_server
import logging
import logging.handlers as handlers
import time_event

def init_cfg():
    return config_loader.load_cfg("etc/config.ini")

def start_taskmgr_server():
    port = config_loader.get_local_addr()
    return taskmgr_server.start(port)

def init():
    if not init_cfg():
        print "failed to initialize cfg module"
        return False
    time_event.post_start_event()
    return True

def logger_init():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    log_dir, log_x, log_y = config_loader.get_log_cfg()
    handler = handlers.RotatingFileHandler(
                  str(log_dir) + "/maze-task.log", mode='a', maxBytes=1024*1024*50, backupCount=5)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

def main(args):
    if not init():
        return
    port = config_loader.get_local_addr()
    logger_init()
    return taskmgr_server.start(int(port))

if __name__ == "__main__":
    main(sys.argv)
    logging.info("quit now!")