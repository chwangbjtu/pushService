#!/usr/bin/python
#-*- coding: utf-8 -*-
import copy
import time
import threading
import logging
import json
import random
import Queue
import hashlib

import db_manager
from maze_task import *
 
generator_mutex = threading.Lock()
init_tid = int(time.time()) + 86400

def generate_tid():
    """generate tid"""
    global generator_mutex
    global init_tid
    generator_mutex.acquire()
    tid = None
    try:
        #if init_tid:
        #    init_tid = int(time.time()) + 86400
        init_tid = init_tid + 1
        rand_num = random.randint(1000, 9999)
        tid = "X%d%d" % (init_tid, rand_num)
    finally:
        generator_mutex.release()
    return tid

def md5(target):
    m = hashlib.md5()
    m.update(target)
    return m.hexdigest()

stat = {}
stat["distribute-submitted"] = 0
stat["package-submitted"]    = 0
stat["transcode-submitted"]  = 0     
class VideoManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._package_task_queue             = Queue.Queue(pow(2, 20))
        self._distribute_task_queue             = Queue.Queue(pow(2, 20))
        self._db_manager             = db_manager.DBManager()
        
        self._videos_lock       = threading.Lock()
        self._videos_map        = {} # all videos here
        self._cloudid_tid_map   = {} # all cloud-id tid pairs here
        
        self._auth_users_lock   = threading.Lock()
        self._auth_users_map    = {} # all auth users here

        self._transcode_lock    = threading.Lock()
        self._transcode_map     = {} # waiting for being submitted to cloud transcoding
        
        self._package_lock      = threading.Lock()
        self._package_map       = {}   # waiting for being submitted to cloud packaging
        
        self._distribute_lock   = threading.Lock()
        self._distribute_map    = {}   # waiting for being submitted to macross distributing
    
    def query_stat_task(self, task):
        _stat = {}
        self._distribute_lock.acquire()
        self._package_lock.acquire()
        self._transcode_lock.acquire()
        self._videos_lock.acquire()
        try:
            _stat["videos-waiting"]         = len(self._videos_map)
            _stat["cloud-id-tid"]           = len(self._cloudid_tid_map)
            _stat["transcode-submitted"]    = stat["transcode-submitted"]
            _stat["transcode-waiting"]      = len(self._transcode_map)
            _stat["package-submitted"]      = stat["package-submitted"]
            _stat["package-waiting"]        = len(self._package_map)
            _stat["distribute-submitted"]   = stat["distribute-submitted"]
            _stat["distribute-waiting"]     = len(self._distribute_map)
            _stat["package-task-queue"]     = self._package_task_queue.qsize()
            _stat["distribute-task-queue"]  = self._distribute_task_queue.qsize()
            return _stat
        finally:
            self._videos_lock.release()
            self._transcode_lock.release()
            self._package_lock.release()
            self._distribute_lock.release()
        
    def _del_one_distribute_task(self, dat_id, distribute_map, videos_map):
        if distribute_map.has_key(dat_id):
            for tid in distribute_map[dat_id]["tid"]:
                if videos_map.has_key(tid):
                    del videos_map[tid]
     
            del distribute_map[dat_id]
                    
    def _compact_maps(self, distribute_map, videos_map, files_map):
        logging.info("move %d file items in files to videos", len(files_map)) 
        for tid in videos_map:
            if files_map.has_key(tid):
                videos_map[tid]["transcode"] = files_map[tid]
  
        logging.info("move video items in video map to distribute map")         
        keys = []
        for dat_id in distribute_map:
            if distribute_map[dat_id]["flag"]:
                keys.append(dat_id)
            else:
                for tid in distribute_map[dat_id]["tid"]:
                    if videos_map.has_key(tid):
                        distribute_map[dat_id]["tid"][tid] = copy.deepcopy(videos_map[tid]) # we do not hope conflict between videos map and distribute map

        logging.info("found %d items from distribute map to compact", len(keys))        
        for dat_id in keys:
            self._del_one_distribute_task(dat_id, distribute_map, videos_map)
        
    def _preprocess_videos(self, all_videos): # submit->transcode->audit->mpacker->distribute
        transcode_map = {}
        package_map   = {}
        cloud_id_tid_map = {}
        for key in all_videos:
            video = all_videos[key]
            if video["cloud_id"]:
                cloud_id_tid_map[video["cloud_id"]] = key
            if video["step"] == "submit":
                transcode_map[key] = copy.deepcopy(video)
            if video["step"] == "audit" and (video["status"] == 1 or video["audit_free"] == 1): # audit free - transcode finished, but do not submit package
                package_map[key]   = copy.deepcopy(video)  
        return [transcode_map, package_map, cloud_id_tid_map]
    
    def load_tasks(self):
        transcode_map   = {}
        cloudid_tid_map = {}
        package_map     = {}
        all_videos      = {}
        distribute_map  = {}
        try:
            distribute_map = self._db_manager.load_distribute_tasks()
            logging.info("%d distribute tasks loaded from db", len(distribute_map) )
            
            all_videos   = self._db_manager.load_all_videos()
            logging.info("%d videos loaded from db", len(all_videos) )
            
            files_map   = self._db_manager.load_transcode_files()
            logging.info("%d transcode files loaded from db", len(files_map) )

            logging.info("before compact [%d %s] distributes/videos loaded from db", len(distribute_map), len(all_videos) )
            self._compact_maps(distribute_map, all_videos, files_map)
            logging.info("after compact [%d %s] distributes/videos loaded from db", len(distribute_map), len(all_videos) )
            
            [transcode_map, package_map, cloudid_tid_map] = self._preprocess_videos(all_videos)
            logging.info("after preprocess [%d %s %s] transcode/package/cloudid-tid-pairs loaded from db", len(transcode_map), len(package_map), len(cloudid_tid_map) )
        except Exception, err:
            logging.warning( "failed to load task from db with err: %s", err )
            # exit 
        self._reload_auth_users()
        
        self._videos_lock.acquire()
        self._videos_map      = all_videos
        self._cloudid_tid_map = cloudid_tid_map       
        self._videos_lock.release()
        
        self._transcode_lock.acquire()
        self._transcode_map     = transcode_map 
        self._transcode_lock.release()
        
        self._package_lock.acquire()
        self._package_map     = package_map 
        self._package_lock.release()
        
        self._distribute_lock.acquire()
        self._distribute_map = distribute_map    
        self._distribute_lock.release()
        
    def _submit_package_tasks(self, tasks):
        for task in tasks:
            try:
                self._package_task_queue.put(NotifyPackageTask(task), block=False)
            except Queue.Full: 
                logging.info("task queue is full ... ")
                del task["submitting"]
                
    def _submit_distribute_tasks(self, tasks):
        for task in tasks:
            try:
                self._distribute_task_queue.put(NotifyDistributeTask(task), block=False)
            except Queue.Full: 
                logging.info("task queue is full ... ")
                del task["submitting"]
                
    def __redo_tasks(self, task_map):
        counter = 0
        tasks = []
        for key in task_map.keys():
            dispatch = task_map[key]
            counter = counter + 1
            now = int(time.time())
            start = 0 if (not dispatch.has_key("tranaction-start-since")) else dispatch["tranaction-start-since"]
            if  now > start and now - start > 30:     
                dispatch["tranaction-start-since"] = now 
                tasks.append(task_map[key])
                
            if counter > 1024 or len(tasks) > 256: # do not lock the map long 
                break
        logging.debug("there are %d tasks found to dispatch ... ", len(tasks) )
        return tasks  
        
    def _redo_distribute_tasks(self):
        self._distribute_lock.acquire()
        try:
            logging.debug("try to resubmit distribute tasks")
            tasks = self.__redo_tasks(self._distribute_map)
            self._submit_distribute_tasks(tasks)
        except Exception, err:
            logging.warning( "failed to resubmit distribute tasks with err: %s", err )
        finally:
            self._distribute_lock.release()
            
    def _redo_package_tasks(self):
        self._package_lock.acquire()
        try:
            logging.debug("try to resubmit package tasks")
            tasks = self.__redo_tasks(self._package_map)
            self._submit_package_tasks(tasks)
        except Exception, err:
            logging.warning( "failed to resubmit package tasks with err: %s", err )
        finally:
            self._package_lock.release()
            
    def redo_dispatch_tasks(self, dispatch_type):
        size = 0
        if dispatch_type == "distribute":
            self._redo_distribute_tasks()
            size = self._distribute_task_queue.qsize()
        elif dispatch_type == "package":
            self._redo_package_tasks()
            size = self._package_task_queue.qsize()
        return size
        
    def _reload_auth_users(self):
        auth_users = self._db_manager.load_auth_users()
        self._auth_users_lock.acquire()
        try:
            if auth_users["result"]:
                logging.debug( "%d auth users now", len(auth_users) - 1)
                self._auth_users_map = auth_users
        except Exception, err:
            logging.warning( "failed to reload auth users %s", err )
        finally:
            self._auth_users_lock.release()
            
    def get_auth_user(self, uid):
        self._auth_users_lock.acquire()
        try:
            username = None if not self._auth_users_map.has_key(uid) else self._auth_users_map[uid]
            return username
        except Exception, err:
            logging.warning( "failed to reload auth users %s", err )
        finally:
            self._auth_users_lock.release()
            
    def run(self):    
        """run the maze thread
        """
        logging.critical( "thread [%s] starts to run ... ", self.getName() )
        last = int(time.time())
        while True:
            time.sleep(600)
            #now = int(time.time())
            try:
                #if now > last and now - last > 600: # update every 10 minutes
                self._reload_auth_users()
            except Exception, err:
                logging.warning( "exception when redoing distribute and package tasks %s", err )
            finally:
                pass
                
        logging.critical( "maze thread [%s] exits", self.getName() )    

    def get_dispatch_task(self, dispatch_type): # task we will dispatch to other peers
        task = None
        task_queue = None
        if dispatch_type == "distribute":
            task_queue = self._distribute_task_queue
        elif dispatch_type == "package":
            task_queue = self._package_task_queue
        
        if not task_queue:
            return None
        try:
            task = task_queue.get_nowait()
        except Queue.Empty:
            pass #logging.debug( "there is no dispatch task" )
        except Exception, err:
            logging.warning( "can not get dispatch task with err: %s", err )
        return task    
    
    def _audit_video_task(self, task):  
        self._package_lock.acquire()
        self._videos_lock.acquire()
        try:
            matched_task                = self._videos_map[task["tid"]]
            matched_task["step"]        = "audit"
            if task["pass"]:
                matched_task["status"] = 1
                matched_task['title']       = task['title']
                matched_task['channel']     = task['channel']
                matched_task['tags']        = task['tags']
                matched_task['description'] = task['description']
                for transcode in matched_task["transcode"]:
                    transcode['logo']        = task['logo']
                    
                logging.debug("submit the task %s to package map for dispatching", task["tid"])
                package_task = copy.deepcopy(matched_task)
                self._package_map[package_task["tid"]] = package_task
            else:
                matched_task["status"] = 2
                del self._videos_map[task["tid"]]
            
        except Exception, err:
            logging.warning("exception when audit video to matched task %s, %s", task["tid"], err)
        finally:
            self._videos_lock.release()
            self._package_lock.release()
            
    def audit_video_task(self, task):
        ret = {"result": True}
        try:
            logging.debug("save audit video %s to db ", task["tid"])    
            ret =  self._db_manager.audit_video_task(task)
            if ret["result"]:
                ret = task  # return the task to client when ok
                ret["result"] = True
                self._audit_video_task(task)
                
        except Exception, err:
            ret["result"] = False
            logging.warning( "failed to add video task with err: %s", err )
        return ret
        
    # add-video    
    def _add_video_task(self, tid, task):
        self._transcode_lock.acquire()
        self._videos_lock.acquire()
        try:
            task["step"]   = "submit"
            task["status"] = 1
            logging.debug("add the video %s to transcode queue", tid)
            self._transcode_map[tid] = copy.deepcopy(task) # one copy to submit transcode
            self._videos_map[tid] = task
            return True
        except Exception, err:
            logging.warning( "failed to add task to transcode map: %s", err )
            return False    
        finally:
            self._videos_lock.release()
            self._transcode_lock.release()
        
    def add_video_task(self, task):
        username = self.get_auth_user(task['uid'])
        if not username: # username should be existed
            return {"result": False}
            
        ret = {"result": True}
        try:
            task["tid"] = md5(json.dumps(task)+generate_tid())
            logging.debug("save new video %s to db ", task["tid"])    
            ret =  self._db_manager.add_video_task(task)
            if ret["result"]:
                ret = task  # return the task to client when ok
                ret["result"] = True
                self._add_video_task(task["tid"], task)
                
        except Exception, err:
            ret["result"] = False
            logging.warning( "failed to add video task with err: %s", err )
        return ret
    
    # get transcode task then submit to cloud transcode    
    def get_transcode_tasks(self, task):
        num = task["num"]
        if num <= 0:
            result = {"result": False, "err": {"code": "00.00", "info": "number is negative"}} 
            return result
        
        self._transcode_lock.acquire()
        tasks = {'result': False}
        try:
            tasks = {'result': True}
            tasks['task_list'] = []
            for key in self._transcode_map.keys():
                transcode = self._transcode_map[key]
                now = int(time.time())
                start = 0 if (not transcode.has_key("tranaction-start-since")) else transcode["tranaction-start-since"]
                if len(tasks['task_list']) < num and ( now > start and now - start > 30 ):
                    self._transcode_map[key]["tranaction-start-since"] = now
                    tasks['task_list'].append(self._transcode_map[key])
            logging.debug("found %d videos for transcoding", len(tasks['task_list']) )
            return tasks    
        except Exception, err:
            logging.warning( "failed to get transcode task from %s", err )
            return tasks
        finally:
            self._transcode_lock.release()
    
    def _is_cloud_id_duplicated(self, task): # duplicated or unknown tid
        self._videos_lock.acquire()
        try:
            return self._cloudid_tid_map.has_key(task['cloud_id']) or (not self._videos_map.has_key(task['tid'])) or (self._videos_map[task['tid']]["cloud_id"])
        except Exception:
            return False
        finally:
            self._videos_lock.release()
            
    def _add_taskid_tid(self, task):
        self._transcode_lock.acquire()
        self._videos_lock.acquire()
        stat["transcode-submitted"] = stat["transcode-submitted"] + 1
        try:
            cloud_id = task['cloud_id']
            tid      = task["tid"]
            self._videos_map[tid]["cloud_id"]   = cloud_id
            self._videos_map[tid]["step"]       = "transcode"
            self._videos_map[tid]["status"]     = 0
            if self._transcode_map.has_key(task["tid"]):
                del self._transcode_map[task["tid"]]
            logging.debug("insert cloud id %s to cloudid-tid map", cloud_id)
            self._cloudid_tid_map[cloud_id]  = tid
        except Exception, err:
            logging.warning("exception when updat  tid, cloud id [%s - %s] %s", tid, cloud_id, err)
        finally:
            self._videos_lock.release()
            self._transcode_lock.release()
            
    # cloud has accept transcode task, task-id returned    
    def add_taskid_tid(self, task):

        ret = {"result": True}
        if self._is_cloud_id_duplicated(task): 
            return ret
        
        try:
            ret = self._db_manager.add_taskid_tid(task) 
            if ret["result"]:
                logging.debug("write cloud id %s to db OK", task['cloud_id'])
                self._add_taskid_tid(task)
            else:
                logging.info("failed to write tid cloud-id map to db %s", task['tid'])
                ret["result"] = False
        except Exception, err:
            logging.warning("exception when update tid - cloud-id [%s-%s] %s", task['tid'], task['cloud_id'], err)

        return ret
    
    # populate the task (it is from client, maybe we can only get task id a.k.a. cloud id)   
    def _update_transcode_when_valid(self, cloud_id, task):
        try:
            self._videos_lock.acquire()
            
            if self._cloudid_tid_map.has_key(cloud_id):
                tid = self._cloudid_tid_map[cloud_id]
                if not self._videos_map.has_key(tid) or self._videos_map[tid]["step"] != "transcode" or self._videos_map[tid]["status"] != 0: # 
                    logging.info("transcode report may be duplicated %s", cloud_id)
                    return False
                logging.debug("find cloud id %s in cloudid tid map", cloud_id)
                matched_task       = self._videos_map[self._cloudid_tid_map[cloud_id]]
                task["tid"]        = matched_task["tid"]
                task["audit_free"] = matched_task["audit_free"]
                task["uid"]        = matched_task["uid"]
                task["priority"]   = matched_task["priority"]
                task["site"]       = matched_task["site"]
                task["channel"]    = matched_task["channel"]        
                return True
            else:
                logging.info("can not find cloud id %s in cloudid tid map", cloud_id)
                return False
        except Exception, err:
            logging.warning("exception when searching matched tid with cloud id %s, %s", cloud_id, err)
            return False
        finally:
            self._videos_lock.release()
            
    def _is_audit_free(self, task):
        return task['audit_free'] == 1
        
    def _add_transcode_report(self, task): # to-do: add task to package map 
        self._package_lock.acquire()
        self._videos_lock.acquire()
        try:
            matched_task                = self._videos_map[task["tid"]]
            matched_task["transcode"]   = task["transcode"]
            matched_task["step"]        = "audit"
            if matched_task["audit_free"]:
                matched_task["status"] = 1
                logging.debug("submit the task %s to package map for dispatching", task["tid"])
                package_task = copy.deepcopy(matched_task)
                #package_task["tranaction-start-since"] = int(time.time())
                #self._submit_package_tasks([package_task])
                self._package_map[package_task["tid"]] = package_task
            else:
                matched_task["status"] = 0
            
        except Exception, err:
            logging.warning("exception when update transcode report to matched task %s, %s", task["tid"], err)
        finally:
            self._videos_lock.release()
            self._package_lock.release()   
            
    # transcode result 
    def add_transcode_report(self, task): # to remove cloudid-tid pair when ok
        try:
            cloud_id = task['cloud_id']
            logging.debug("update task by cloud id (%s)", cloud_id)
            if not self._update_transcode_when_valid(cloud_id, task): 
                return {"result": False}
            
            logging.debug("write transcode result to db...")
            if task.get('result') and task['result']:
                ret = self._db_manager.add_transcode_report(task)   # failed transcode should be considered
                if ret["result"]:
                    self._add_transcode_report(task)
            else:
                logging.debug("task [tid = %s] failed ", task['tid'])
                ret =  self._db_manager.set_transcode_fail(task)
                
            if not ret["result"]:
                logging.info("failed to handle transcode report (%s)", json.dumps(task))
                return {"result": False}
            else:
                return {"result": True}
        except Exception, err:
            logging.warning("exception when handling transcode report: %s", str(err))
            return {"result": False}
    
    def _set_package_start(self, task):
        self._package_lock.acquire()
        self._videos_lock.acquire()
        try:
            stat["package-submitted"] = stat["package-submitted"] + 1
            if self._package_map.has_key(task["tid"]): 
                del self._package_map[task["tid"]]
            matched_task = self._videos_map[task["tid"]]
            matched_task["step"]   = "mpacker"
            matched_task["status"] = 0
        except Exception, err:
            logging.warning("exception when update package report to matched task %s, %s", task["tid"], err)
        finally:
            self._videos_lock.release()
            self._package_lock.release() 
            
    def set_package_start(self, task):
        try:
            logging.debug("task [tid = %s] start to be packaged", task['tid'])
            ret = self._db_manager.set_package_start(task) 
            if ret["result"]:
                self._set_package_start(task)
            return {"result": True} 
        except Exception, err:
            logging.warning("exception when set package start status %s", str(err))
            return {"result": False}
            
    # get tids (task is from client, maybe we can only get task id a.k.a. cloud id)     
    def _find_matched_tids(self, cloud_id_list):
        tid_map = {}
        self._videos_lock.acquire()
        try:    
            for cloud_id in cloud_id_list:
                if self._cloudid_tid_map.has_key(str(cloud_id)):
                    tid = self._cloudid_tid_map[str(cloud_id)]
                    matched_task = None if (not self._videos_map.has_key(tid)) else self._videos_map[tid]
                    if matched_task: #and ((matched_task["step"] == "mpacker" and matched_task["status"] == 0) or (matched_task["step"] == "audit" and 0 == matched_task["status"])):
                        tid_map[tid] = tid
                else:
                    logging.info("can not find tid for cloud id %s", cloud_id)
            return tid_map
        except Exception, err:
            logging.warning("exception whent find matched tid ... %s", err)
            return tid_map
        finally:
            self._videos_lock.release()
            
    def _add_package_report(self, task): 
        try:
            all_videos = {}
            self._distribute_lock.acquire()
            self._videos_lock.acquire()
            for tid in task["tid"]:
                if self._videos_map.has_key(tid):
                    matched_task = self._videos_map[tid]
                    #if (matched_task["step"] == "audit" and 0 == matched_task["status"]) or (matched_task["step"] == "mpacker" and matched_task["status"] == 0):
                    matched_task["step"] == "mpacker"
                    matched_task["status"] = 1
                    all_videos[tid] = copy.deepcopy(matched_task)
            if len(all_videos) > 0:
                task["tid"] = all_videos
                #task["tranaction-start-since"] = int(time.time())
                #self._submit_distribute_tasks([task])
                self._distribute_map[task["infohash"]] = task
        except Exception, err:
            logging.warning("exception when update package report to matched task %s, %s", task["tid"], err)
        finally:
            self._videos_lock.release()
            self._distribute_lock.release()    
    
    def _is_package_ok(self, task):
        return (task.get('result') and task.get('infohash') and task.get('size') and task.get('server_ip') and task.get('server_port') and task.get('task_id'))    
    
    def add_package_report(self, task):
        try:
            cloud_id_list = task['task_id']
            task['tid']      = self._find_matched_tids(cloud_id_list) # duplicated report is considered
            if len(cloud_id_list) != len(task['tid']): # may be this is a duplicated report
                logging.debug("there are some tids not found ... \n%s\n%s", json.dumps(cloud_id_list), json.dumps(task['tid']))
            if not len(task['tid']):
                return {"result": True}
                
            if self._is_package_ok(task):
                ret = self._db_manager.add_package_report(task)
                if not ret["result"]:
                    logging.info("can not add package to db") 
                    return {"result": False}
                else:
                    logging.debug("add package report to db ok, now distribute it infohash - %s ", task["infohash"])
                    self._add_package_report(task)
            else:
                ret = self._db_manager.set_package_fail(task) # now not update memory
            return {"result": True}
        except Exception, err:
            logging.warning("exception when transfering cloud tid funshionid map: %s", str(err))
            return {"result": False}
    
    def _set_distribute_start(self, task):
        self._distribute_lock.acquire()
        self._videos_lock.acquire()
        try:
            stat["distribute-submitted"] = stat["distribute-submitted"] + 1
            if self._distribute_map.has_key(task["infohash"]):
                del self._distribute_map[task["infohash"]]
            for tid in task["tid"]:
                if self._videos_map.has_key(tid):
                    if self._videos_map[tid].has_key("cloud_id") and self._cloudid_tid_map.has_key(self._videos_map[tid]["cloud_id"]):
                        del self._cloudid_tid_map[self._videos_map[tid]["cloud_id"]]
                    del self._videos_map[tid]
                else:
                    logging.info("tid %s not found in video map", tid)
            return True
        except Exception, err:
            logging.warning( "failed to remove task from distribute map %s", err )
            return False    
        finally:
            self._videos_lock.release()
            self._distribute_lock.release()
         
    def set_distribute_start(self, task):
        try:
            ret =  self._db_manager.set_distribute_start(task)
            if ret["result"]:
                self._set_distribute_start(task)
            return True
        except Exception, err:
            logging.warning( "failed to remove task from distribute map %s", err )
            return False    
            
    def apply_audit_task(self, task):
        task = task
        return None
    
    def add_audit_report(self, task):
        task = task
        return None
        
    def cancel_audit_task(self, task):
        task = task
        return None
    
    @staticmethod
    def get_video_manager():
        return video_manager

#singleton - video manager
video_manager = VideoManager()

def get_video_manager():
    return video_manager
    
