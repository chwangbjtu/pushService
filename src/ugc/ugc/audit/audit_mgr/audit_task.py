#!/bin/env python
# -*- coding: utf-8    -*-
import json

class AuditTask(object):
     def __init__(self, tid, uid, title, tags, channel, step, funshion_id, time, duration, username, vid, priority):
         self._tid = tid
         self._uid = uid
         self._title = title
         self._tags = tags
         self._channel = channel
         self._step = step
         self._funshion_id = funshion_id
         self._funshion_list = []
         self._funshion_list.append(funshion_id)
         #self._funshion_list = ""
         #self._funshion_list += "%s," % (funshion_id)
         self._time = time
         self._duration = duration
         self._username = username
         self._vid = vid
         self._priority = priority
         #self._rate = rate

     def add_funshion(self, funshion_id):
         self._funshion_list.append(funshion_id)


     def todict(self):
        try:
            
            return {"tid":self._tid, "uid":self._uid,  "title":self._title, "tags":self._tags, "channel":self._channel, "step":self._step, "funshion_id":self._funshion_list, "time":self._time, 
                   "duration":self._duration, "username":self._username, "vid":self._vid, "priority":self._priority, }

        except Exception,e:
            return None


class TaskList(object):
     def __init__(self):
         self._task_list = []
         self._map_tid = {}
         #self._map_task[tid] = audit_task

     def add_task(self, audit_task):
         try:
             tid = audit_task._tid
             if  self._map_tid.has_key(tid):
                 print 'yes enter.'
                 task =  self._map_tid[tid]
                 funsh_id = audit_task._funshion_id
                
                 task._funshion_list.append(funsh_id)
                 
                 return True
             self._map_tid[tid] = audit_task
             self._task_list.append(audit_task.todict())
             return True
         except Exception,e:
             print 'error',e 
             return False


     def tolist(self):
         try:
             return self._task_list
         except Exception,e:
             return None



if __name__ == "__main__":
    
    task = AuditTask(tid='1', uid=1, title = 'sdfsfs1', tags = 'tags', channel='china', step='task-manager', funshion_id='1212ffffffffff', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)

    print task.todict()

    tlist = TaskList()
    tlist.add_task(task)
    task = AuditTask(tid='2', uid=1, title = 'sdfsfs2', tags = 'tags', channel='china', step='task-manager', funshion_id='12', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)
    tlist.add_task(task)
    task = AuditTask(tid='4', uid=1, title = 'sdfsfs3', tags = 'tags', channel='china', step='task-manager', funshion_id='212eeeeeee', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)
    tlist.add_task(task)
    task = AuditTask(tid='2', uid=1, title = 'sdfsfs2', tags = 'tags', channel='china', step='task-manager', funshion_id='34', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)
    tlist.add_task(task)
    task = AuditTask(tid='2', uid=1, title = 'sdfsfs2', tags = 'tags', channel='china', step='task-manager', funshion_id='567', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)
    tlist.add_task(task)

    task = AuditTask(tid='4', uid=1, title = 'sdfsfs3', tags = 'tags', channel='china', step='task-manager', funshion_id='ffffff', time='2013', duration=12112, username='zhou', vid='v1232', priority=45)
    tlist.add_task(task)
    print tlist.tolist()
    
    '''
    list = []
    list.append('abc')
    list.append('defg')
    list.append('kkkkk')
    temp = ""
    print list
    for item in list:
        temp += "%s" % item

    print temp
    '''