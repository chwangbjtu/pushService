# -*- coding:utf-8 -*-
from multiprocessing import Process
from multiprocessing import Pipe
from tornado import log
import traceback
import sys
from common.conf import Conf
from parse import parse
from http_server import HttpServer 
class parse_server(object):

    def __init__(self):
        self._modules = []
        self._procs = []

    def register_module(self):

        http_server = HttpServer(Conf.server_port)
        http_server.register_api('parse', parse())
        self._modules.append(http_server)
        
        #self._modules.append(UrlCheckProc(interval = Conf.urlcheck_proc_sleep_time))

    def start_module(self):
        for m in self._modules:
            print 'start proc'
            proc = Process(target=m)
            proc.start()
            self._procs.append(proc)

    def join(self):
        for proc in self._procs:
            proc.join()

    def start(self):
        try:
            self.register_module()
            self.start_module()
            self.join()
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    helper = parse_server()
    helper.start()
