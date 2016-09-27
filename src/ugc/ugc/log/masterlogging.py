#!/usr/bin/python
# -*- coding:utf-8 -*- 
import threading
import logging
import datetime
import os
import platform

class MasterLogging(object):
    '''the log file will automatically be divided by date,such as 2012-12-14.log,2012-12-15.log, '''
    
    __today = None
    __file_handler = None
    __lock_day = threading.Lock()
    __lock_create = threading.Lock()
    __instance = None
    __logger = logging.getLogger("master_logger")
    __log_dir = "."
    __output_dict = {
                      logging.DEBUG:(logging.Logger.debug,"debug"),
                      logging.INFO:(logging.Logger.info,"info"),
                      logging.WARNING:(logging.Logger.warn,"warning"),
                      logging.ERROR:(logging.Logger.error,"error"),
                      logging.CRITICAL:(logging.Logger.critical,"critical")
                      }

    @staticmethod
    def instance():
        if not MasterLogging.__instance:
            MasterLogging.__lock_create.acquire()
            if not MasterLogging.__instance:
                MasterLogging.__instance = object.__new__(MasterLogging)
                object.__init__(MasterLogging.__instance)
            MasterLogging.__lock_create.release()
        return MasterLogging.__instance

    def __init__(self,log_dir):
        "disable the __init__ method"

    def initialize(self,logdir = ".",filter_level=logging.NOTSET,output_to_console = False):
        self.__log_dir = logdir
        #check this directory
        if not os.path.isdir(self.__log_dir):
            try:
                os.mkdir(self.__log_dir)
            except OSError:
                return False
        if platform.system() != "Windows" and not os.access(self.__log_dir,os.R_OK|os.W_OK|os.X_OK):
            return False
        self.__logger.setLevel(filter_level)
        if output_to_console:
            stream_handler = logging.StreamHandler()
            self.__logger.addHandler(stream_handler)
        return True

    def log_str(self,level,infos):
        self.__lock_day.acquire()
        now = datetime.datetime.now()
        today = now.date()
        if today != self.__today:
            if self.__file_handler:
                self.__logger.removeHandler(self.__file_handler)
                self.__file_handler.close()
            filename = today.isoformat() + ".csv"
            filename = self.__log_dir + "/" + filename
            self.__today = today
            self.__file_handler = logging.FileHandler(filename)
            self.__logger.addHandler(self.__file_handler)
        self.__lock_day.release()
        value = self.__output_dict[level]
        func = value[0]
        flag = value[1]
        import thread
        thread_id = thread.get_ident()
        output_str = now.isoformat() + ','+"[%d],"%thread_id + flag + ',' + infos + ',,,'
        func(self.__logger,output_str)

def debug(text):
    MasterLogging.instance().log_str(logging.DEBUG,text)
def info(text):
    MasterLogging.instance().log_str(logging.INFO,text)
def warn(text):
    MasterLogging.instance().log_str(logging.WARNING,text)
def error(text):
    MasterLogging.instance().log_str(logging.ERROR,text)
def critical(text):
    MasterLogging.instance().log_str(logging.CRITICAL,text)

def initialize(logdir = ".",filter_level="debug",output_to_console = False):
    level_dict = {"all":logging.NOTSET,"debug":logging.DEBUG,"info":logging.INFO,\
                    "warnning":logging.WARNING,"error":logging.ERROR,"critical":logging.CRITICAL}
    try:
        return MasterLogging.instance().initialize(logdir,level_dict[filter_level],output_to_console)
    except Exception,e:
        print e.message
        return False

#just for testing
if __name__ == '__main__':
    initialize(output_to_console=True)
    for i in range(0,10,1):
        debug("I'm here as always")
        info("I'm here as always")
        warn("I'm here as always")
        error("I'm here as always")
        critical("I'm here as always")
        os.system("pause")
