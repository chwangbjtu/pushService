#!/usr/bin/python
# -*- coding:utf-8 -*-
import logging
import json

class Cycle(object):
    """State Machine. It's not designed for multi-thread!!!!"""
    def __init__(self):
        self.__require_task_pending = False
        self.__conns = 0
        self.__exiting = False
        self.__task_cache = []
        self.__task_count = 0
        self.__timeout = None

    def set_exit(self):
        logging.debug("set exiting to true")
        self.__exiting = True

    def exiting(self):
        return self.__exiting

    def add_conn(self,count=1):
        logging.debug("increase %d connection", count)
        self.__conns += count

    def sub_conn(self,count=1):
        logging.debug("decrease %d connection", count)
        self.__conns -= count

    def conn(self):
        return self.__conns

    def set_pending(self,pending=True):
        logging.debug("set pending to %s", str(pending))
        self.__require_task_pending = pending

    def pending(self):
        return self.__require_task_pending

    def add_task(self,task_obj):
        logging.debug("add one task")
        self.__task_cache.append(task_obj)

    def sub_task_ref(self,count=1):
        logging.debug("decrease %d task reference", count)
        self.__task_count -= count

    def add_task_ref(self,count=1):
        logging.debug("increase %d task reference", count)
        self.__task_count += count

    def get_task(self):
        if not self.__task_cache:
            return None
        logging.debug("pop one task")
        return self.__task_cache.pop()

    def task_count(self):
        return self.__task_count

    def timeout(self):
        return self.__timeout

    def set_timeout(self,timeout):
        self.__timeout = timeout

    def get_all_task(self):
        return self.__task_cache

    def pack_map_obj(self):
        map_obj = {"connections":self.__conns,"exiting":self.__exiting,
                   "cached_count":len(self.__task_cache),"total_task_count":self.__task_count}
        task_list = []
        for item in self.__task_cache:
            task_obj = item.pack_map_obj()
            task_list.append(task_obj)
        map_obj["cache_tasklist"] = task_list
        return map_obj

cycle = Cycle()
