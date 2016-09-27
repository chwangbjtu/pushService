#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
    To process incoming requests with policy manager

"""
import threading
import copy
import logging
import json
import time
import hashlib
import urllib2
import random
import Queue

import sys
import parser
import down_load


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
        #rand_num = random.randint(1000, 9999)
        tid = "%d" % init_tid
    finally:
        generator_mutex.release()
    return tid

def md5(target):
    m = hashlib.md5()
    m.update(target)
    return m.hexdigest()
    
def ok_200(body):
    return "HTTP/1.1 200 OK\r\nConnection:Close\r\nContent-Length:%d\r\n\r\n%s" % (len(body), body)
    
def not_found_404():
    return "HTTP/1.1 404 Not Found\r\nConnection:Close\r\nContent-Length:0\r\n\r\n"
    
def not_found_403():
    return "HTTP/1.1 403 Not Found\r\nConnection:Close\r\nContent-Length:0\r\n\r\n"

    
class PostTask:
    def __init__(self, url, body, delay):
        self._url = url
        self._body = body
        self.trigger = int(time.time()) + delay
        
    def _post_request(self):
        _opener = urllib2.build_opener()
        response = None
        code = -1
        try:
            print self._url, "\n", self._body
            server_url = self._url
            response = _opener.open(server_url, self._body, timeout = 30)
            code = response.getcode()
        except Exception, error:
            print self._url, "\n", self._body, "\nexception: ", error
        else:
            content = response.read()
            response.close()
            print content
        
    def execuate(self):
        self._post_request()

class PostDownloadTask(PostTask):
    def __init__(self, url, body, delay, following_task):
        PostTask.__init__(self, url, body, delay)
        self.follower = following_task
        self.trigger = int(time.time()) + delay
    def _post_request(self):
        """http visitor ,method post"""

        try:
            urllist = parser.get_video_url(self._body)
            url = urllist[0]
            now = str(int(time.time()))
            down_load.download(url,"./"+now,1000)
            #print self._body
            #print urllist
            print "recv over"
        except Exception, e:
            print e
        
    def execuate(self):
        self._post_request()
        if self.follower: 
            self.follower.execuate()
        
    
class WorkerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self._task_queue             = Queue.Queue(pow(2, 20))
        
    def put_task(self, task):
        try:
            #print "put task in queue"
            self._task_queue.put(task)
            return True
        except Queue.Full :
            #logging.warning( "dispatch task queue is full, " )
            return False
        except Exception, err:
            #logging.warning( "can not get dispatch task with err: %s", err )
            return False
            
    def run(self):
        
        while True:
            task = None
            try:
                task = self._task_queue.get_nowait()
            except Queue.Empty:
                pass #logging.debug( "there is no dispatch task" )
            except Exception, err:
                logging.warning( "can not get dispatch task with err: %s", err )
            if not task:
                time.sleep(1)
                continue
            now = int(time.time())
            if task.trigger <= now:
                #print task.trigger, now
                task.execuate()
            else:
                time.sleep(1)
                self.put_task(task)
            
worker_thread =  WorkerThread()
worker_thread.start()
       
class RequestHandler:
    _DIGEST_KEY = "funshion.com"
    _server_conf = {
            "retCode": 200,  
            "retMsg": "some config for ls/cs", 
        }
    _ls_list = [{"server_id":1,"server_ip":"127.0.0.1","server_port":"8888","controll_ip":"192.168.16.118","controll_port":"9000"},{"server_id":2,"server_ip":"127.0.0.1","server_port":"8888","controll_ip":"127.0.0.2","controll_port":"8889"}]
    _cs_list = [{"server_id":1,"server_ip":"127.0.0.1","server_port":"8888","controll_ip":"192.168.16.118","controll_port":"8888"}]
    #_cs_list = [{"server_id":1,"server_ip":"127.0.0.1","server_port":"8888","controll_ip":"192.168.16.118","controll_port":"8889"}]

    _ios_task = {  
           "app_type": "ipad",
           "content":    u"\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u4E00\u4E8C\u4E09\u56DB\u4E94\u516D\u4E03\u516B\u4E5D\u5341\u4E00\u4E8C",     
           "alert":    "424",
           "badge" :   "10",     
           "msg_id":   " 5 ",
           "sound":    "",
           "ios_url":  "1",
           #"device":  ["c5167e16796efb6fc52ccf86b5cebd50d9a2aa1c5e46f20895513df018d79480","43e55facaf1fc8e68422a9fa4a12cc2d65a23bb377a2a22c983a1b14f1b70b76"]
           #"device":  ["43e55facaf1fc8e68422a9fa4a12cc2d65a23bb377a2a22c983a1b14f1b70b76","43e55facaf1fc8e68422a9fa4a12cc2d65a23bb377a2a22c983a1b14f1b70b76","0000000000000000000000000000000000000000000000000000000000000000"] 
           "device":  ["43e55facaf1fc8e68422a9fa4a12cc2d65a23bb377a2a22c983a1b14f1b70b76"]*1
        }
    
    _android_task = {
            "msg_id":           "123",
            "app_type":         "aphone",
            "cmd_id":           "3",
            "para":             "mid:123",
            "url":              "",
            "show_time":        "123",
            "content":          "",
            "device": ["000000000001", "000000000002"]
        }
    _reysys_task = {
        "push_end_time": "1482106890", 
        "app_type": ["aphone", "ipad", "funshionTv","iphone"], 
        #"app_type": ["funshionTv"], 
        "show_time": "1382067477", 
        "push_type": "resy", 
        "push_begin_time": "1384311664",
        "algorithm":
        {
            "mediabased":
            {
                "a":"time_domain_tag_correlation",
                "b":"tag2_correlation"
                #"a":"time_domain_tag_correlation"
            },
            "timebased":
            {
                 "a":"user_history_based",
                 #"b":""
            }
        }, 
        "msg_list": [
            {
                "sound": "", 
                "android_content": u"\u76d8\u70b9\u90a3\u4e9b\u7535\u5f71\u4e2d\u6700\u7f8e\u4e3d\u7684\u5973\u4eba\uff0c\u8c01\u662f\u4f60\u5fc3\u4e2d\u7684\u5973\u795e\uff1f", 
                "media_id": "105257", 
                "android_msg_type": "short", 
                "picture": "http://img.funshion.com/attachment/new_images/2013/10-18/48518145_1382063843_868.jpg", "android_jump_flag": "yes", "msg_id": "575", 
                "content": u"\u76d8\u70b9\u90a3\u4e9b\u7535\u5f71\u4e2d\u6700\u7f8e\u4e3d\u7684\u5973\u4eba\uff0c\u8c01\u662f\u4f60\u5fc3\u4e2d\u7684\u5973\u795e\uff1f", 
                "ios_msg_type": "mpurl", 
                "cmd_id": "3", 
                "media_type": "media", 
                "android_url": "http://jobsfe.funshion.com/play/v1/mp4/1F64EF26FBEEDE1404AA48D3C87112CE81A3EBF4.mp4?file=0ebe0ab4bc4fe34fa2612904aaeb3c9e794a7892.mp4&f=z&clifz=aphone", 
                "title": u"\u98ce\u884c\u7535\u5f71", 
                "ios_url": "http://jobsfe.funshion.com/play/", 
                "badge": "0",
                "tag":[{"tag": u"\u5DE7\u864E", "weight": 1},{"tag":u"\u4EB2\u5B50","weight":"10"}]
                #"media_tag":{u"\u8F6C\u5316":"1"}\u60A8\u8981\u8F6C\u6362\u7684\u6C49\u5B57
            }, 
            {
                "sound": "", 
                "android_content": u"\u3010\u8f7b\u677e\u4e00\u523b\u30112013\u5e74\u86cb\u75bc\u89c6\u9891\u96c6\u9526top60\uff0c\u8ba9\u4f60\u7b11\u5230\u7206\uff01", 
                "media_id": "90588", 
                "android_msg_type": "short", 
                "picture": "http://img.funshion.com/attachment/new_images/2013/10-18/48518145_1382063321_767.jpg", 
                "android_jump_flag": "yes", 
                "msg_id": "574", 
                "content": u"\u3010\u8f7b\u677e\u4e00\u523b\u30112013\u5e74\u86cb\u75bc\u89c6\u9891\u96c6\u9526top60\uff0c\u8ba9\u4f60\u7b11\u5230\u7206\uff01", "ios_msg_type": "mpurl", 
                "cmd_id": "3", 
                "media_type": "media", 
                "android_url": "http://jobsfe.funshion.com/play/v1/mp4/F0D6226A3DE2DC6AAABFD2FCB54ADC1336809C7C.mp4?file=243960_standard.mp4&f=z&clifz=aphone", 
                "title": u"\u98ce\u884c\u7535\u5f71", 
                "ios_url": "http://jobsfe.funshion.com/play/", 
                "badge": "0",
                "tag":[{"tag":u"\u67F3\u5CA9","weight":"10"},{"tag": u"\u60A8\u8981\u8F6C\u6362\u7684\u6C49\u5B57", "weight": 1}]
                #"media_tag":{u"\u8F6C\u5316":"1"}
            }, 
            {
                "sound": "", 
                "android_content": u"\u3010\u8f7b\u677e\u4e00\u523b\u30112013\u5e74\u86cb\u75bc\u89c6\u9891\u96c6\u9526top60\uff0c\u8ba9\u4f60\u7b11\u5230\u7206\uff01", 
                "media_id": "88888", 
                "android_msg_type": "short", 
                "picture": "http://img.funshion.com/attachment/new_images/2013/10-18/48518145_1382063321_767.jpg", 
                "android_jump_flag": "yes", 
                "msg_id": "575", 
                "content": u"\u3010\u8f7b\u677e\u4e00\u523b\u30112013\u5e74\u86cb\u75bc\u89c6\u9891\u96c6\u9526top60\uff0c\u8ba9\u4f60\u7b11\u5230\u7206\uff01", "ios_msg_type": "mpurl", 
                "cmd_id": "3", 
                "media_type": "media", 
                "android_url": "http://jobsfe.funshion.com/play/v1/mp4/F0D6226A3DE2DC6AAABFD2FCB54ADC1336809C7C.mp4?file=243960_standard.mp4&f=z&clifz=aphone", 
                "title": u"\u98ce\u884c\u7535\u5f71", 
                "ios_url": "http://jobsfe.funshion.com/play/", 
                "badge": "0",
                "tag":[{"tag":u"\u60A8\u8981\u8F6C\u6362\u7684\u6C49\u5B57","weight":"10"},{"tag": u"\u60A8\u8981\u8F6C\u6362\u7684\u6C49\u5B57", "weight": 1}]
                #"media_tag":{u"\u8F6C\u5316":"1"}
            }
        ],
        "push_id": "resy_3"
    }

    _reysys_test_task = {
        "push_id": "resy_5",
        #"app_type":["aphone","iphone", "funshionTv","ipad"],
        "app_type":["funshionTv","ipad"],
        "algorithm":
        {
            "mediabased":
            {
                "a":"tag2_correlation",
                "b":"time_domain_tag_correlation"
            },
            "timebased":
            {
                 "a":"user_history_based",
                 #"b":""
            }
        },
        "msg_list":
        [
             {
                 "media_id":"105257",
                 "media_type":"media",
                 "tag":[{"tag":u"\u6BCD\u72D7\u4E3B\u4EBA\u62A5\u8B66","weight":"10"}]
             },
             {
                 "media_id":"90588",
                 "media_type":"media",
                 #"tag":[{"tag":u"\u6BCD\u72D7\u4E3B\u4EBA\u62A5\u8B66","weight":"10"},{"tag": u"\u9AD8\u5706\u5706\u9AD8\u5706\u5706", "weight": 1}]
                 "tag":[{"tag":u"\u6BCD\u72D7\u4E3B\u4EBA\u62A5\u8B66","weight":"10"}]
             }
        ],
        "user_num":"1000"
    }


    _empty_task = ""
    _URL_CLOUD_ADD_TASK     = "/add_task/"
    _URL_CLOUD_NOTIFY_PACK  = "/notify_pack_dat/"
    _URL_QUERY_MGMT_CONF    = "/api"
    _URL_QUERY_MGMT_CONF2   = "/api/"
    _URL_QUERY_MGMT_TASK    = "/mgmt"
    _URL_QUERY_TEST_TASK    = "/test"
    _URL_QUERY_REYSYS_TASK  = "/test"
    _URL_NOTIFY_MS_LOAD     = "/macross/" # this is used by transcoder to notify ms to load packeaged dat file for distribution 
    def summary(self):
        ret = {}
        ret["received_android_task_num"] = self.received_android_task_num
        ret["waiting_android_tasks_num"] = self.waiting_android_tasks_num
        ret["waiting_ios_tasks_num"]     = self.waiting_ios_tasks_num
        ret["next_waiting_task"]         = {"type": self.next_waiting_task}
        if self.next_waiting_task == "ios":
            ret["next_waiting_task"]["number"] = 1
            ret["next_waiting_task"]["task"] = self._ios_task
        if self.next_waiting_task == "android":
            ret["next_waiting_task"]["number"] = 1
            ret["next_waiting_task"]["task"] = self._android_task
        if self.next_waiting_task == "batch-ios":
            ret["next_waiting_task"]["number"] = self.waiting_ios_tasks_num
            ret["next_waiting_task"]["task"] = self._ios_task
        if self.next_waiting_task == "batch-android":
            ret["next_waiting_task"]["number"] = self.waiting_android_tasks_num
            ret["next_waiting_task"]["task"] = self._android_task
        ret["prev_task_received"]         = self.prev_task_received 
        return ret
        
    def __init__(self):
        self._command_handlers = {}
        self._command_handlers[self._URL_QUERY_MGMT_CONF]      = self.handle_query_mgmt_conf
        self._command_handlers[self._URL_QUERY_MGMT_CONF2]      = self.handle_query_mgmt_conf
        self._command_handlers[self._URL_QUERY_MGMT_TASK]      = self.handle_query_mgmt_task
        self._command_handlers[self._URL_QUERY_TEST_TASK]      = self.handle_query_test_task
        
        self._command_handlers[self._URL_CLOUD_ADD_TASK]       = self.handle_add_could_task
        self._command_handlers[self._URL_CLOUD_NOTIFY_PACK]    = self.handle_notify_could_pack
        self._command_handlers[self._URL_NOTIFY_MS_LOAD]       = self.handle_notify_ms_load
        self.next_waiting_task          = None
        self.prev_task_received         = None
        self.received_android_task_num  = 0
        self.waiting_android_tasks_num  = 0
        self.waiting_ios_tasks_num      = 0
        self._logger = logging.getLogger()
    def handle_notify_ms_load(self, request):
        return ok_200('return=ok\nadd task success')
    def handle_notify_could_pack(self, request):
        content = json.loads(request.body)
        notify_url = content["pack_result_notify"]
        task_id = content["task_id"]
        _report_packaging = {
            "result" : True,
            "infohash": generate_tid(), 
            "size": 123456,
            "server_ip": "121.12.101.131",
            "server_port": "8888",
            "task_id":task_id
        }

        worker_thread.put_task(PostTask(notify_url, json.dumps(_report_packaging), 1))
        return ok_200(json.dumps({"success":True, "data":{"message":"okokokok"}}))
    def handle_add_could_task(self, request):
        _task_id = generate_tid()
        _report_transcoding = {
                "task_id" : _task_id,
                "result" : True,
                "data" : [
                    {
                        "rate" : 800,
                        "img_url" : ["http://host:port/path/to/pic_0.jpg"], 
                        "video_url": "http://host:port/path/to/video.mp4",
                        "funshion_id": md5(str(_task_id)),
                        "size": 123456,
                        "milliseconds": 123456,
                        "definition": "smooth",
                        "filename": "this is file name"
                    }
                ],
                "error_message":"okok"
            }
        
        content = json.loads(request.body)
        source_url = content["source_url"] 
        #info = json.loads(source_url)
        #print info["vid"]
        notify_url = content["notify_url"]
        report_transcoding = PostTask( notify_url, json.dumps(_report_transcoding), 0)
        download_media = PostDownloadTask(source_url, source_url, 2, report_transcoding) 
        worker_thread.put_task( download_media )
        # download_media.start()
        
        return ok_200(json.dumps({"success":"ok", "data":{"task_id":_task_id}}))
    def handle_query_mgmt_conf(self, request):
        cmd   = request.arguments["cmd"][0]

        if cmd == "report_video":
            return ok_200("return=ok")
        cli   = request.arguments["cli"][0]
        ctime = request.arguments["ctime"][0]
        sign  = request.arguments["sign"][0]
        server_conf = copy.copy(self._server_conf)
        if sign != md5(cli + cmd + ctime + self._DIGEST_KEY):
            server_conf["retCode"] = 416
            print server_conf
            return ok_200(json.dumps(server_conf))
        
        if cmd == "get_ls_list":
            server_conf["retCode"] = 200
            server_conf["result"] = self._ls_list
            return ok_200(json.dumps(server_conf))
        elif cmd == "get_cs_list":
            server_conf["retCode"] = 200
            server_conf["result"] = self._cs_list
            return ok_200(json.dumps(server_conf))
        elif cmd == "get_recommend_push":
            server_conf["retCode"] = 200
            server_conf["result"] = self._reysys_task
            server_conf["result"] = ""
            print server_conf
            return ok_200(json.dumps(server_conf))
        elif cmd == "get_offline_push":
            server_conf["retCode"] = 200
            server_conf["result"] = self._reysys_test_task
            print self._reysys_test_task
            #server_conf["result"] = ""
            #print server_conf
            return ok_200(json.dumps(server_conf))
        else:
            server_conf["retCode"] = 404
            return ok_200(json.dumps(server_conf))
        
    def handle_query_mgmt_task(self, request):
        cmd   = request.arguments["cmd"][0]
        if cmd == "pop_msg":
            import random
            task = {"return": "notfound", "content": {}}
            if self.next_waiting_task == "ios":
                task["return"]= "ok"
                task["content"]= self._ios_task 
                self.next_waiting_task = None
            elif self.next_waiting_task == "batch-ios" and self.waiting_ios_tasks_num > 0:
                task["return"]= "ok"
                task["content"]= self._ios_task
                self.waiting_ios_tasks_num -= 1
            elif self.next_waiting_task == "android": 
                task["return"]= "ok"
                task["content"]= self._android_task
                self.next_waiting_task = None 
            elif self.next_waiting_task == "batch-android"  and self.waiting_android_tasks_num > 0: 
                task["return"]= "ok"
                task["content"]= self._android_task
                self.waiting_android_tasks_num -= 1
                
            #print "notification task replied to provider %s" % (json.dumps(task))
            return ok_200(json.dumps(task))
        elif cmd == "push_msg":
            cmd   = request.arguments["cmd"][0]
            ctime = request.arguments["ctime"][0]
            sign  = request.arguments["sign"][0]
            if sign != md5(cmd + ctime + self._DIGEST_KEY):
                return ok_200("return=error\r\nerrinfo=digest error")
                
            body = request.body 
            task = json.loads(body)
            task["app_type"]
            self.prev_task_received = task
            self.received_android_task_num += 1
            print "android notification task received from provider %s" % (json.dumps(task))
            return ok_200("return=ok")
        elif cmd == "push_recsys_msg":
            recsys = {}
            recsys["return"] = "ok"
            return ok_200(json.dumps(recsys))
        elif cmd == "push_recsys_token":
            recsys = {}
            recsys["return"] = "ok"
            print request.body
            return ok_200(json.dumps(recsys))
    def handle_query_test_task(self, request):
        resp = {"cmd-state":"cmd ok"}
        cmd   = request.arguments["cmd"][0]
        if cmd == "reset-test":
            self.next_waiting_task         = None
            self.received_android_task_num = 0
            self.prev_task_received        = None
            self.waiting_android_tasks_num = 0
            self.waiting_ios_tasks_num     = 0
        if cmd == "one-ios-task":
            self.next_waiting_task = "ios"
        if cmd == "one-android-task":
            self.next_waiting_task = "android"
        if cmd == "batch-ios-tasks":
            self.next_waiting_task = "batch-ios"
            self.waiting_ios_tasks_num = int(request.arguments["number"][0])
        if cmd == "batch-android-tasks":
            self.next_waiting_task = "batch-android"
            self.waiting_android_tasks_num = int(request.arguments["number"][0])
        if cmd == "check-task-state":
            resp["summary"] = self.summary()

        return ok_200(json.dumps(resp, indent=4))    
    #main entry#
    def handle_request(self, request):
        _debug = "incoming request: %s" % (request.uri)
        print _debug 
        if request.body:
            print request.body
        #print request
        url = request.path.lower()
        if not self._command_handlers.has_key(url):
            _info = "Not supported request: %s" % (url) 
            print _info 
            return not_found_404()
            
        handler = self._command_handlers[url]
        message = ""
        try:
            message = handler(request)
        except Exception, err:
            print err
            message = ""
        return message

if __name__ == "__main__":
    pass



