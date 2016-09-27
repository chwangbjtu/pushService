#!/usr/bin/python
# -*- coding:utf-8 -*-  
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop

import time
import sys
import logging
import logging.handlers
import etc
import http_server

def logger_init():
    logger = logging.getLogger()
    if etc.DEBUG: 
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    log_file = "master.log"
    handler = logging.handlers.RotatingFileHandler(
                  etc.LOGPATH + log_file, mode='a', maxBytes=1024*1024*etc.MAX_LOGFILE_SIZE, backupCount=5)
    #print "Note: log file will be written to " + etc.LOG_DIR + log_file
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

def main():
    logger_init()

    server = http_server.HttpServer()
    server.start(etc.SERVICE_PORT)

if __name__ == "__main__":
    main()
