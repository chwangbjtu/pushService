# -*- coding:utf-8 -*-
from tornado import log
import traceback

import pymongo
import gridfs

import sys
import time
sys.path.append('.')
from common.conf import Conf

class MongoConnect(object):

    def __init__(self):
        self.client = None
        self.db_conn = None
        self.db_fs = None

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
            #self.client = pymongo.MongoClient(host=Conf.mg_host, port=Conf.mg_port)
            self.client = pymongo.MongoClient(host='192.168.177.3', port=27017)
            self.db_conn = getattr(self.client, 'xv')
            self.db_conn.authenticate('xv', 'xv')
            self.db_fs =  gridfs.GridFS(self.db_conn)
            return True
        except Exception, e:
            print "connect error:",e
            #log.app_log.error(str(e))
            return False

    def connect_local_mongo(self):
        try:
            self.client = pymongo.MongoClient(host='192.168.16.113', port=30000)
            self.db_conn = getattr(self.client, 'test')
            self.db_conn.authenticate('user', '')
            self.db_fs =  gridfs.GridFS(self.db_conn)
            return True
        except Exception, e:
            print "connect_local_mongo error:",e
            #log.app_log.error(str(e))
            return False

    def reconnect(self):
        try:
            log.app_log.error('++reconnect db')
            while True:
                if not self.ping():
                    self.connect()
                else:
                    break
                time.sleep(1)
            log.app_log.error('++reconnected db')
                
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def put_object(self, data, **kwargs):
        try:
            return self.db_fs.put(data, **kwargs)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def get_object(self, obj_id):
        try:
            return self.db_fs.get(obj_id)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

    def find_object(self, **kwargs):
        try:
            return self.db_fs.find_one(kwargs)
        except Exception, e:
            log.app_log.error(traceback.format_exc())

if __name__ == "__main__":

    try:
        conn = MongoConnect()
        if conn:
            data = 'hello world'
            meta = {'vid': '888'}
            content_type = 'txt'
            _id = conn.put_object(data, **meta)
            print _id
            obj = conn.get_object(_id)
            print obj._id
            obj2 = conn.find_object(**meta)
            print obj2._id
    except Exception as e:
        log.app_log.error("Exception: %s" % traceback.format_exc())
