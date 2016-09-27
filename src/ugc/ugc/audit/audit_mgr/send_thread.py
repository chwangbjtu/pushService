#!/usr/bin/python
# -*- coding:utf-8 -*- 
import time
import threading
import task_queue
import http_client
import log
import etc
import cloud_helper

class SendThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__queue = task_queue.TaskQueue.instance()
        self._log_error = log.MakeLog(etc.error_for_process)
        self._log_error.start()
        self._task_q = task_queue.TaskQueue.instance()


    def post_crane(self, task_item):
        try:
            method = "/crane/?cmd=examresult"
            (code, response) = http_client.post(task_item._ip, task_item._port, method, task_item._send_str)
            if code != 200:
                err_info = "post_crane post ip: %s, port: %s, error code: %d, res:%s" % (task_item._ip, task_item._port, code, response)
                print err_info
                self._log_error.logerror(err_info)
                self._task_q.add_task(task)
            print 'post to crane %s, %s, %s, %s ok.' % (ip, port, method, send_json)
            return True
        except Exception, err:
            err_info = "post_crane Error Reason: %s" % (err)
            print err_info
            self._log_error.logerror("exception in post_crane." + err_info)
            return False


    def post_cloud_Centaurus(self, task):
        try:
            send_str = cloud_helper.produce_cloud_pack(task._task_id)
            if send_str == None:
                return False
            (code, response) = http_client.post(etc.CLOUD_SERVICE_IP, etc.CLOUD_SERVICE_PORT,etc.cloud_notify_pack_dat, send_str)
            if code != 200:
                err_info = "post has err with post_cloud_Centaurus ip: %s, port:%s, res:%s" % (etc.CLOUD_SERVICE_IP, etc.CLOUD_SERVICE_PORT, response)
                print err_info
                self._log_error.logerror(err_info)
                self._task_q.add_task(task)
            print 'post_cloud_Centaurus ip: %s, port:%s, %s ok.' % (etc.CLOUD_SERVICE_IP, etc.CLOUD_SERVICE_PORT, send_str)
            return True
        except Exception, err:
            err_info = "post_cloud_Centaurus Error Reason: %s" % (err)
            print err_info
            self._log_error.logerror("exception in post_cloud_Centaurus." + err_info)
            return False

    
    def run(self):
        while True:
            try:
                tqs = self.__queue.size()
                task_item = None
                try:
                    task_item = self.__queue.get_task()
                    if task_item == None:
                        #print 'none , sleep 1 s.'
                        time.sleep(1)
                        continue
                    #self.post_crane(task_item)   # for crane
                    print 'cloud task id : ', task_item._task_id
                    self.post_cloud_Centaurus(task_item)
                except Exception, e:
                    print 'process error in send_thread, ',e
                    continue
            except Exception,e:
                print 'Exception error ', e
                continue
