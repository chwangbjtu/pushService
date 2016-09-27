#-*- coding: utf-8 -*-
import threading
import json  
import time  
import logging
import etc
from common import http_download
from common import idmgr 
class Chtbt(threading.Thread):
    def __init__(self,interval):  
        threading.Thread.__init__(self)  
        self.interval = interval
        self.htbturl = "http://" + str(etc.master_domain) + "/heartbeat?" + "broker_port=" + str(etc.service_port) + "&id="
        self.httpdownloader = http_download.HTTPDownload()
        self.idmgr = idmgr.Idmgr.instance()
   
    def run(self):
        while True: 
            try:
                data = ""
                hurl = self.htbturl
                id = self.idmgr.get_id()
                if id:
                    hurl = hurl + str(id)
                data = self.httpdownloader.get_data(hurl)
            except Exception, e:
                #logging.log(logging.ERROR, traceback.format_exc())
                logging.error(traceback.format_exc())
            finally:
                info = "htbt url is : %s,result is : %s" % (hurl,data,)
                logging.info(info)
            
            time.sleep(self.interval)  

if __name__ == "__main__":
    htbt = Chtbt(10)
    htbt.start()
