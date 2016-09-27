#!/usr/bin/python
# -*- coding:utf-8 -*-  
#import tornado.httpserver
#import tornado.web
#import tornado.options
#import tornado.ioloop

import time
import sys
import logging
import logging.handlers
import etc
import visitor
import tlogger
#import http_server
#import taskmanager
#import filelist_manager
#import clean_manager


if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    print "path is:",os.path.dirname(os.path.dirname(path))
    sys.path.append(os.path.dirname(os.path.dirname(path)))


import youtube_dl



def logger_init():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    #logger.setLevel(logging.INFO)
    
    log_file = "youtube.log"
    handler = logging.handlers.RotatingFileHandler(
                  etc.LOGPATH + log_file, mode='a', maxBytes=1024*1024*50, backupCount=5)
    #print "Note: log file will be written to " + etc.LOG_DIR + log_file
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def download(id):
    res = -1
    try:
        logging.debug("download id is:" + str(id))
        if id == None or len(id) == 0:
            return res
        url1 = "https://www.youtube.com/watch?v=" + id

        import subprocess
        filename = etc.DATA_PATH+id
        p = subprocess.Popen(["./youtube-dl","-o",filename,url1])
        while True:
            tres = None
            tres =  p.poll()
            if tres != None:
                time.sleep(1)
            else:
                p.wait()
                res = 0
                break

    except Exception, err:
        logging.error(str(err))

    return res


def main():
    logger_init()
    tvisitor = visitor.visitor()
    site = ""
    task_id = ""
    ret = ""
    vid = ""
    (task_id,vid,site) = tlogger.tlogger.instance().getlog()
    first = True
    while True:
        try:
            if first and task_id != None and site != None and vid != None:
                first = False
            else:
                (site,task_id,vid) = tvisitor.get_msg()
            #(site,task_id,vid) = tvisitor.get_msg()
            if not task_id or not vid:
                time.sleep(10)
                logging.error("task_id or site is null")
                continue
            if len(task_id) == 0 or len(site) == 0 or len(vid) == 0:
                time.sleep(10)
                logging.error("task_id or site is null")
                continue

            logging.info("task_id is %s,site is %s",task_id,site)
            res = 1
            if site == "youtube":
                tlogger.tlogger.instance().writelog(task_id,vid,site)
                for i in range(etc.retry_num):
                    res = download(vid)
                    if res == 0:
                        break
            
            if res != 0:
                ret = "1"
            else:
                ret = "0" 
        except Exception, err: 
            logging.error("youtube error:" + str(err))
            time.sleep(1)
            ret = "1"
        logging.debug("ret is %s",ret)
        try:
            #if ret == "0" and len(vid) != 0:
            if len(vid) != 0:
                logging.error("task_id:" + task_id + ",vid is " + str(vid) + " ,ret is %s" + ret)
                tvisitor.download_ok(task_id,vid)
                logging.error("task_id:" + task_id + ",vid is " + str(vid) + " ,ret is %s" + ret)
            else:
                logging.error("task_id:" + task_id + ",vid is " + str(vid) + " ,ret is %s" + ret)
        except Exception, err:
            logging.error("download_ok error:" + str(err))


if __name__ == "__main__":
    main()
