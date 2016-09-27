# -*- coding:utf-8 -*-
from multiprocessing import Process, Array, Manager
from multiprocessing import Pipe
from tornado import log
import traceback
import sys
from http.http_server import HttpServer
from service.base_service import BaseService
from sender.maze_sender import MazeSender
from sender.linda_sender import LindaSender
from sender.flashget_sender import Flashget_Sender
from common.conf import Conf
from sender.queue_mgr import QueuesManager

class DataServer(object):
    def __init__(self):
        self._procs = []

    def start(self):
        try:
            #queue manager
            q_mgr = QueuesManager.get_instance()

            #http/service pipe
            http_pipe, service_pipe = Pipe()

            proc = Process(target=BaseService(q_mgr, service_pipe))
            self._procs.append(proc)
            log.app_log.debug("start service ...")

            #http server
            log.app_log.debug("start http on port %s ..." % Conf.server_port)
            proc = Process(target=HttpServer(Conf.server_port, q_mgr, http_pipe))
            self._procs.append(proc)

            #sender
            if Conf.use_linda:
                proc = Process(target=LindaSender(q_mgr, Conf.add_linda_task_url))
                self._procs.append(proc)
            else:
                proc = Process(target=MazeSender(q_mgr, Conf.add_maze_task_url,Conf.add_maze_task_url_addr))
                self._procs.append(proc)
            #flashget
            proc = Process(target=Flashget_Sender(q_mgr, Conf.add_flashget_task_url,Conf.add_flashget_task_url_addr))
            self._procs.append(proc)

            #start
            for proc in self._procs:
                proc.start()

            #join
            for proc in self._procs:
                proc.join()
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":
    yks = DataServer()
    yks.start()
