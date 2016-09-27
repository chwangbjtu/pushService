# -*- coding:utf-8 -*-
from multiprocessing import Process, Array, Manager
from tornado import log
import traceback
import sys
from common.conf import Conf
from sender.sender import Sender
from http.http_server import HttpServer
from sender.mem_queue import MemQueue
from sender.redis_queue import RedisQueue

class VideoPushServer(object):
    def __init__(self):
        self._procs = []

    def _get_queue(self, qname):
        if Conf.enable_redis:
            return RedisQueue(qname)

        return MemQueue(qname)

    def start(self):
        try:
            tq = self._get_queue('vps_q')
            if not tq.ping():
                log.app_log.error("start data server error: cannot connect to redis.")
                return

            conf = Conf()

            #sender
            proc = Process(target=Sender(tq, conf.add_maze_task_url))
            self._procs.append(proc)
            log.app_log.debug("start sender ...")

            #http server
            log.app_log.debug("start http on port %s ..." % conf.server_port)
            proc = Process(target=HttpServer(conf, tq))
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
    ts = VideoPushServer()
    ts.start()
