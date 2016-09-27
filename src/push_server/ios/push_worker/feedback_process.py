#-*- coding: utf-8 -*-
from multiprocessing import Process
from apnslib.notify_mgr import *
from api import http_client
import etc
import time
from tornado import log

class FeedbackProcess(Process):
    def __init__(self, cert):
        Process.__init__(self)
        self._feedback = APNSFeedbackWrapper(cert, False)
        
    def run(self):  
        while True:
            try:
                tokens = []
                tokens = self._feedback.receive()
                if tokens:
                    _client = http_client.HttpClient()
                    log.app_log.info("feedback process delete tokens")
                    _client.del_token(tokens)
                
                time.sleep(5)
            
            except Exception,e:
                print e
          
if __name__ == '__main__':
    #ipad_process = FeedbackProcess(etc.IPAD_CERT)
    #iphone_process = FeedbackProcess(etc.IPHONE_CERT)
    funshiontv_process = FeedbackProcess(etc.FUNSHIONTV_CERT)
    #ipad_process.start()
    #iphone_process.start()
    funshiontv_process.start()
    