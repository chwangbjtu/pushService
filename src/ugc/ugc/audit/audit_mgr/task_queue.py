#!/usr/bin/python
# -*- coding:utf-8 -*- 

import Queue


class TaskSendInfo(object):
     def __init__(self, ip, port, send_str):
         self._ip = ip
         self._port = port
         self._send_str = send_str

class CloudTask(object):
     def __init__(self, task_id):
         self._task_id = task_id


class TaskQueue(object):
    @classmethod
    def instance(cls):
        """instance"""
        if not hasattr(cls, "_ins"):
            cls._ins = cls()
        return cls._ins

    def __init__(self):
        self._task_q = Queue.Queue()       #for task queue.


    def add_task(self, task):
        try:
            self._task_q.put(task)
            return True
        except Exception,e:
            return False
    
    def get_task(self):
        try:
            item = self._task_q.get_nowait()
            return item
        except Queue.Empty:
            return None

    def size(self):
        tqs = self._task_q.qsize()
        return tqs

if __name__ == "__main__":
    task = TaskSendInfo('127.0.0.1','80','zhousdfssf')
    task_q = TaskQueue.instance()
    task_q.add_task(task)
    print 'size: ', task_q.size()
    item = task_q.get_task()
    print item._ip, item._port, item._send_str, task_q.size()