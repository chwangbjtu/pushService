#!/usr/bin/python
# -*- coding:utf-8 -*- 
import logging
import threading

class Idmgr:
    # Global lock for creating global Idmgr instance
    _lock = threading.Lock()
    _id = None

    def __init__(self):
        pass

    @staticmethod
    def instance():
        if not hasattr(Idmgr, "_instance"):
            Idmgr._lock.acquire()
            if not hasattr(Idmgr, "_instance"):
                Idmgr._instance = Idmgr()
            Idmgr._lock.release()
        return Idmgr._instance

    def set_id(self,id):
        self._id = id
    
    def get_id(self):
        return self._id

    def clear_id(self):
        self._lock.acquire()
        self._id = None
        self._lock.release()
