#!/usr/bin/python
# -*- coding:utf-8 -*-  

import time
import sys
import os
#import log
import logging
import logging.handlers
from common import http_download
import etc
import htbt
import downloader

def init_db_dir():
    if os.path.exists("./log"):
        pass
    else:
        logging.info("create db path: %s", "./log")
        os.mkdir("./log")

def logger_init():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.handlers.RotatingFileHandler("./log/" + "youtube_downloader.log", mode='a', maxBytes=1024*1024*50, backupCount=5)
    formatter = logging.Formatter('%(asctime)s, %(levelname)s %(filename)s:' + '%(funcName)s:%(lineno)d: %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

def main():
    init_db_dir()
    logger_init()

    chtbt = htbt.Chtbt(etc.htbt_interval)
    chtbt.start()
    
    cdownloader = downloader.Cdownloader()
    cdownloader.start()

    while True:
        time.sleep(86400)

if __name__ == "__main__":
    main()

