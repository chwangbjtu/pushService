#!/usr/bin/python
# -*- coding:utf-8 -*-  

"""Control log function."""

import etc
import os.path
import logging
import logging.handlers

class MakeLog:
    '''Log module.

    Log to the screen and the file with level.'''


    def __init__(self, filename):
        self.__logfilename = filename
        pass

    def start(self):
        """Start the log module."""
        
        if os.path.exists(etc.LOGPATH):
            pass
        else:
            os.mkdir(etc.LOGPATH)
        self.logger = logging.getLogger(self.__logfilename)
        
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s]%(message)s[file:%(filename)s,func:%(funcName)s,line:%(lineno)d]")
        
        self.logger.setLevel(logging.DEBUG)
        filepathname = etc.LOGPATH + self.__logfilename + ".log"
        fh = logging.handlers.TimedRotatingFileHandler(filepathname, 'D', 1, 7)
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def loginfo(self, content):
        self.logger.info(content)

    def logerror(self, content):
        self.logger.error(content)
		
if __name__ == "__main__":
    log = MakeLog("ta")
    log.start()
    log.loginfo("aaaaaaaaaa")
    log.logerror("aaaaaaaaaa")


