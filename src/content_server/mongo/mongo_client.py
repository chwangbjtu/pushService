# -*-coding:utf-8 -*-
import pymongo
import time
from tornado import log
import traceback
from common.conf import Conf

class MongoConnect(object):
    def __init__(self):
        self.client = None
        self.db_conn = None

        self.connect()

    def __del__(self):
        if self.client:
            self.client.close()

    def ping(self):
        try:
            return self.client.alive()
        except Exception, e:
            return False

    def close(self):
        try:
            if self.client:
                self.client.close()
                self.client = None
                
            return True
        except Exception, e:
            return False

    def connect(self):
        try:
            hosts = []
            if Conf.mg_host:
                hosts_tmp = Conf.mg_host.split(',')
                for host in hosts_tmp:
                    host = host.strip()
                    hosts.append(host)
            self.client = pymongo.MongoClient(host=hosts, connect=False)
            self.db_conn = getattr(self.client, Conf.mg_name)
            self.db_conn.authenticate(Conf.mg_user, Conf.mg_password)
            return True
        except Exception, e:
            self.client = None
            self.db_conn = None
            log.app_log.error(str(e))
            return False
            
    def reconnect(self):
        try:
            times = 0
            while Conf.mg_retry_time > times:
                if not self.ping():
                    self.connect()
                else:
                    break
                time.sleep(1)
                times += 1
            
            log.app_log.error('reconnected times [%d]' % (times))

        except Exception, e:
            log.app_log.error(traceback.format_exc())
    
    def get_conn(self):
        if not self.db_conn:
            self.reconnect()
            
        return self.db_conn
            