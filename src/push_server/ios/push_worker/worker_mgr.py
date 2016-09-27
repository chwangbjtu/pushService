#-*- coding: utf-8 -*-
import etc
import worker_thread
import feedback_process
from tornado import options
from tornado import log

options.parse_config_file('etc.py')

class WorkerMgr(object):
    def __init__(self):
        self._process = {}
        self._feedback_process = {}
        self._process_num = etc.WORKER_NUM
    
    def start(self):
        for k in range(0, self._process_num):
            self._process[k] = worker_thread.WorkerThread()
            self._process[k].start()
        
        if etc.open_feedback == 1:
            for cert in etc.CERT_LIST:
                self._feedback_process[cert] = feedback_process.FeedbackProcess(cert)
                self._feedback_process[cert].start()
     
if __name__ == "__main__":
    worker_mgr = WorkerMgr()
    worker_mgr.start()
    